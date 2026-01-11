import os
import re
import sys
import shutil
import hashlib
import requests
import questionary
from rich.console import Console
from rich.progress import Progress
import subprocess

console = Console()

PKGBUILD_TEMPLATE = """# Maintainer: ewgsta <ewgst@proton.me>
pkgname=weeb-cli
pkgver={version}
pkgrel=1
pkgdesc="Tarayıcı yok, reklam yok, dikkat dağıtıcı unsur yok. Sadece siz ve eşsiz bir anime izleme deneyimi."
arch=('any')
url="https://github.com/ewgsta/weeb-cli"
license=('CC-BY-NC-ND-4.0')
depends=('python' 'python-typer' 'python-rich' 'python-questionary' 'python-requests')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
source=("https://files.pythonhosted.org/packages/source/${{pkgname::1}}/$pkgname/$pkgname-$pkgver.tar.gz")
sha256sums=('{sha256}')

build() {{
    cd "$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}}

package() {{
    cd "$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
}}
"""

def run_command(command, cwd=None, shell=True, silent=False):
    # Use errors='replace' to handle encoding issues safely
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell, 
            capture_output=True, 
            text=True,
            errors='replace' 
        )
    except Exception as e:
        raise Exception(f"Command execution failed: {e}")

    if result.returncode != 0:
        if not silent:
            console.print(f"[red]Komut hatası: {command}[/red]")
            err_output = (result.stderr or "").strip() or (result.stdout or "").strip()
            console.print(err_output)
        raise Exception((result.stderr or "").strip() or (result.stdout or "").strip())
    
    return (result.stdout or "").strip()

def get_current_version():
    with open("pyproject.toml", "r") as f:
        content = f.read()
        match = re.search(r'version = "(.*?)"', content)
        return match.group(1) if match else "0.0.0"

def update_version(new_version):
    with open("pyproject.toml", "r") as f:
        content = f.read()
    
    new_content = re.sub(r'version = ".*?"', f'version = "{new_version}"', content)
    
    with open("pyproject.toml", "w") as f:
        f.write(new_content)
        
    # Also update __init__.py
    with open("weeb_cli/__init__.py", "w") as f:
        f.write(f'__version__ = "{new_version}"')

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    import errno, stat
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

def generate_src_info(pkgbuild_content):
    # Simple regex-based parser
    def get_val(key):
        match = re.search(f"{key}=['\"]?([^'\"\n]+)['\"]?", pkgbuild_content)
        return match.group(1) if match else ""
    
    def get_arr(key):
        match = re.search(rf"{key}=\(([^)]+)\)", pkgbuild_content)
        if not match: return []
        # Return matched string items, preserving structure for simple print
        return match.group(1).replace("'", "").replace('"', "").split()

    pkgname = get_val("pkgname")
    pkgver = get_val("pkgver")
    pkgrel = get_val("pkgrel")
    pkgdesc = get_val("pkgdesc")
    url = get_val("url")
    license_val = get_val("license")
    
    # We construct source manually as regex for variable expansion inside PKGBUILD is hard
    # Relying on standard format from template
    source = f"https://files.pythonhosted.org/packages/source/{pkgname[0]}/{pkgname}/{pkgname}-{pkgver}.tar.gz"
    
    sha256sums = get_arr("sha256sums")[0]
    
    return f"""pkgbase = {pkgname}
	pkgdesc = {pkgdesc}
	pkgver = {pkgver}
	pkgrel = {pkgrel}
	url = {url}
	arch = any
	license = {license_val}
	makedepends = python-build
	makedepends = python-installer
	makedepends = python-wheel
	makedepends = python-setuptools
	depends = python
	depends = python-typer
	depends = python-rich
	depends = python-questionary
	depends = python-requests
	source = {source}
	sha256sums = {sha256sums}

pkgname = {pkgname}
"""

def publish_aur(version):
    console.print(f"\\n[blue]📦 AUR Paketi (v{version}) hazırlanıyor...[/blue]")
    
    # Generate distribution tarball locally to calculate hash
    # Note: In real scenarios, PyPI source hash matches local build if repeatable, 
    # but best practice implies waiting for PyPI. For now we assume local sdist matches.
    if os.path.exists("dist"):
        shutil.rmtree("dist", onerror=handle_remove_readonly)
    
    run_command("python -m build --sdist")
    
    dist_file = f"dist/weeb-cli-{version}.tar.gz"
    if not os.path.exists(dist_file):
         # Try underscore match (python sdist often normalizes names)
         dist_file = f"dist/weeb_cli-{version}.tar.gz"
    
    sha256 = calculate_sha256(dist_file)
    console.print(f"[dim]SHA256: {sha256}[/dim]")
    
    # Update PKGBUILD
    pkgbuild_content = PKGBUILD_TEMPLATE.format(version=version, sha256=sha256)
    
    aur_dir = "aur_temp"
    if os.path.exists(aur_dir):
        shutil.rmtree(aur_dir, onerror=handle_remove_readonly) # Use shutil for cross-platform recursive delete
        
    try:
        run_command(f"git clone ssh://aur@aur.archlinux.org/weeb-cli.git {aur_dir}")
        
        # Clean repository content (remove old files like package.json)
        for item in os.listdir(aur_dir):
            if item == ".git": continue
            path = os.path.join(aur_dir, item)
            if os.path.isdir(path):
                shutil.rmtree(path, onerror=handle_remove_readonly)
            else:
                os.unlink(path)
        
        with open(os.path.join(aur_dir, "PKGBUILD"), "w", encoding="utf-8") as f:
            f.write(pkgbuild_content)
            
        # Generate .SRCINFO manually without makepkg
        src_info = generate_src_info(pkgbuild_content)
        with open(os.path.join(aur_dir, ".SRCINFO"), "w", encoding="utf-8") as f:
            f.write(src_info)
        
        run_command("git add -A", cwd=aur_dir)
        run_command(f'git commit -m "Update to {version}"', cwd=aur_dir)
        run_command("git push origin HEAD:master", cwd=aur_dir)
        
        console.print("[green]✅ AUR Yayını Başarılı![/green]")
    except Exception as e:
        console.print(f"[red]❌ AUR Yayını Başarısız: {e}[/red]")
    finally:
         if os.path.exists(aur_dir):
            shutil.rmtree(aur_dir, onerror=handle_remove_readonly)

def main():
    console.clear()
    console.print("[bold cyan]🚀 Weeb CLI Python Yayınlayıcı[/bold cyan]\n")
    
    current_version = get_current_version()
    console.print(f"Mevcut Versiyon: [bold]{current_version}[/bold]")
    
    bump_type = questionary.select(
        "Versiyonlama seçeneği:",
        choices=[
            "Patch (x.x.Y)",
            "Minor (x.Y.x)",
            "Major (Y.x.x)",
            "Değişiklik yapma (Mevcut versiyon)"
        ]
    ).ask()
    
    if bump_type == "Değişiklik yapma (Mevcut versiyon)":
        new_version = current_version
    else:
        major, minor, patch = map(int, current_version.split("."))
        if "Patch" in bump_type: patch += 1
        elif "Minor" in bump_type: minor += 1; patch = 0
        elif "Major" in bump_type: major += 1; minor = 0; patch = 0
        new_version = f"{major}.{minor}.{patch}"
        
        console.print(f"\n[yellow]Yeni versiyon: {new_version}[/yellow]")
        if questionary.confirm("Bu versiyonu onaylıyor musunuz?").ask():
            update_version(new_version)
            run_command("git add pyproject.toml weeb_cli/__init__.py")
            run_command(f'git commit -m "chore: bump version to {new_version}"')
        else:
            console.print("[red]İptal edildi.[/red]")
            return

    # Trigger GitHub Workflow via Tag
    if questionary.confirm("GitHub'a Tag pushlansın mı? (Bu işlemi Release Workflow'u başlatacak)").ask():
        tag_name = f"v{new_version}"
        try:
            # Check if tag exists locally or remote? simple try catch
            run_command(f"git tag {tag_name}")
            run_command(f"git push origin {tag_name}")
            
            # Dynamically get current branch to push
            current_branch = run_command("git rev-parse --abbrev-ref HEAD")
            run_command(f"git push origin {current_branch}")
            
            console.print("[green]✅ Tag pushlandı ve Workflow tetiklendi![/green]")
        except Exception as e:
            console.print(f"[red]⚠️ Tag hatası (muhtemelen zaten var): {e}[/red]")

    # Distributions
    actions = questionary.checkbox(
        "Hangi platformlar için yerel dosyalar/işlemler güncellensin?",
        choices=[
            "AUR (PKGBUILD Push)",
            "Homebrew (Formula Güncelle)",
            "Scoop (Manifest Güncelle)",
            "Chocolatey (Nuspec Güncelle)"
        ]
    ).ask()
    
    if "AUR (PKGBUILD Push)" in actions:
        publish_aur(new_version)
        
    # Get SHA256 of sdist for Homebrew (Source based)
    # We recalculate or reuse if available.
    dist_file = f"dist/weeb-cli-{new_version}.tar.gz"
    if not os.path.exists(dist_file):
        dist_file = f"dist/weeb_cli-{new_version}.tar.gz"
    
    # Ensure dist exists if we skipped AUR
    if not os.path.exists(dist_file):
        run_command("python -m build --sdist")
        if not os.path.exists(dist_file):
             dist_file = f"dist/weeb_cli-{new_version}.tar.gz"
    
    sdist_sha256 = calculate_sha256(dist_file)

    if "Homebrew (Formula Güncelle)" in actions:
        publish_homebrew(new_version, sdist_sha256)
        
    if "Scoop (Manifest Güncelle)" in actions:
        publish_scoop(new_version)
    
    if "Chocolatey (Nuspec Güncelle)" in actions:
        publish_chocolatey(new_version)

    console.print("\n[bold green]✨ İşlem Tamamlandı![/bold green]")


def push_to_git_repo(repo_url, branch, file_operations_callback, platform_name):
    console.print(f"[blue]🚀 {platform_name} deposuna gönderiliyor...[/blue]")
    temp_dir = f"{platform_name.lower()}_temp"
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, onerror=handle_remove_readonly)
        
    try:
        run_command(f"git clone {repo_url} {temp_dir}")
        
        # Perform file copies
        file_operations_callback(temp_dir)
        
        run_command("git add -A", cwd=temp_dir)
        
        # Check if there are changes
        status = run_command("git status --porcelain", cwd=temp_dir)
        if not status:
            console.print(f"[yellow]⚠️ {platform_name} için değişiklik yok, atlanıyor.[/yellow]")
            return

        run_command(f'git commit -m "Update weeb-cli to latest version"', cwd=temp_dir)
        run_command(f"git push origin {branch}", cwd=temp_dir)
        console.print(f"[green]✅ {platform_name} Yayını Başarılı![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ {platform_name} Hatası: {e}[/red]")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, onerror=handle_remove_readonly)

def publish_homebrew(version, sha256):
    console.print(f"\n[blue]🍺 Homebrew Formülü (v{version}) hazırlanıyor...[/blue]")
    
    content = f"""class WeebCli < Formula
  include Language::Python::Virtualenv

  desc "Tarayıcı yok, reklam yok. Sadece sen ve anime."
  homepage "https://github.com/ewgsta/weeb-cli"
  url "https://files.pythonhosted.org/packages/source/w/weeb-cli/weeb-cli-{version}.tar.gz"
  sha256 "{sha256}"
  license "CC-BY-NC-ND-4.0"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end
end
"""
    # Ask for Repo if not configured (mock interaction for now, assuming standard or asking)
    repo_url = questionary.text("Homebrew Tap Repo URL:", default="https://github.com/ewgsta/homebrew-tap.git").ask()
    if not repo_url: return

    def copy_ops(target_dir):
        # Homebrew taps usually store formula in Formula/ directory or root
        formula_dir = os.path.join(target_dir, "Formula")
        if not os.path.exists(formula_dir) and os.path.exists(os.path.join(target_dir, "lib")):
             # Maybe it's a root repo, but standard taps have Formula directory
             os.makedirs(formula_dir)
        
        # If Formula dir doesn't exist and it's an empty repo, create it
        if not os.path.exists(formula_dir):
             os.makedirs(formula_dir, exist_ok=True)

        with open(os.path.join(formula_dir, "weeb-cli.rb"), "w", encoding="utf-8") as f:
            f.write(content)

    push_to_git_repo(repo_url, "main", copy_ops, "Homebrew")

def publish_scoop(version):
    console.print(f"\n[blue]🍨 Scoop Manifest (v{version}) hazırlanıyor...[/blue]")
    
    content = f"""{{
    "version": "{version}",
    "description": "Tarayıcı yok, reklam yok. Sadece sen ve anime.",
    "homepage": "https://github.com/ewgsta/weeb-cli",
    "license": "CC-BY-NC-ND-4.0",
    "architecture": {{
        "64bit": {{
            "url": "https://github.com/ewgsta/weeb-cli/releases/download/v{version}/weeb-cli-Windows.exe",
            "hash": "check" 
        }}
    }},
    "bin": "weeb-cli-Windows.exe",
    "checkver": "github",
    "autoupdate": {{
        "architecture": {{
            "64bit": {{
                "url": "https://github.com/ewgsta/weeb-cli/releases/download/v$version/weeb-cli-Windows.exe"
            }}
        }}
    }}
}}"""
    
    repo_url = questionary.text("Scoop Bucket Repo URL:", default="https://github.com/ewgsta/scoop-bucket.git").ask()
    if not repo_url: return

    def copy_ops(target_dir):
        # Scoop buckets usually have manifest in root or bucket/ folder
        bucket_dir = os.path.join(target_dir, "bucket")
        target_file = ""
        if os.path.exists(bucket_dir):
            target_file = os.path.join(bucket_dir, "weeb-cli.json")
        else:
            target_file = os.path.join(target_dir, "weeb-cli.json")
            
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)

    push_to_git_repo(repo_url, "main", copy_ops, "Scoop")

def publish_chocolatey(version):
    console.print(f"\n[blue]🍫 Chocolatey Paketi (v{version}) hazırlanıyor...[/blue]")
    
    base_dir = "distribution/chocolatey"
    tools_dir = os.path.join(base_dir, "tools")
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir, onerror=handle_remove_readonly)
    os.makedirs(tools_dir, exist_ok=True)
    
    nuspec_content = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd">
  <metadata>
    <id>weeb-cli</id>
    <version>{version}</version>
    <title>Weeb CLI</title>
    <authors>ewgsta</authors>
    <projectUrl>https://github.com/ewgsta/weeb-cli</projectUrl>
    <tags>weeb-cli anime cli</tags>
    <summary>Tarayıcı yok, reklam yok. Sadece sen ve anime.</summary>
    <description>Terminal tabanlı profesyonel anime izleme aracı.</description>
    <licenseUrl>https://github.com/ewgsta/weeb-cli/blob/main/LICENSE</licenseUrl>
  </metadata>
  <files>
    <file src="tools\\**" target="tools" />
  </files>
</package>"""

    install_script = f"""$ErrorActionPreference = 'Stop';
$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$url        = "https://github.com/ewgsta/weeb-cli/releases/download/v{version}/weeb-cli-Windows.exe"
# Hash check skipped, assuming GitHub Release integrity
Get-ChocolateyWebFile -PackageName 'weeb-cli' `
                      -FileFullPath "$toolsDir\\weeb-cli.exe" `
                      -Url $url

Install-BinFile -Name "weeb-cli" -Path "$toolsDir\\weeb-cli.exe"
"""

    with open(os.path.join(base_dir, "weeb-cli.nuspec"), "w", encoding="utf-8") as f:
        f.write(nuspec_content)
        
    with open(os.path.join(tools_dir, "chocolateyInstall.ps1"), "w", encoding="utf-8") as f:
        f.write(install_script)
    
    # Pack and Push
    try:
        console.print("[dim]Chocolatey Pack...[/dim]")
        run_command("choco pack", cwd=base_dir)
        
        if questionary.confirm("Chocolatey'e PUSH komutu çalıştırılsın mı? (API Key ayarlı olmalı)").ask():
            # Find the nupkg
            for file in os.listdir(base_dir):
                if file.endswith(".nupkg"):
                    nupkg_path = file
                    break
            
            console.print(f"[blue]Chocolatey Push ({nupkg_path})...[/blue]")
            run_command(f"choco push {nupkg_path} --source https://push.chocolatey.org/", cwd=base_dir)
            console.print("[green]✅ Chocolatey Yayını Başarılı![/green]")
        else:
            console.print("[yellow]ℹ️ Chocolatey paketlendi ama pushlanmadı.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]❌ Chocolatey Hatası: {e}[/red]")
        console.print("[yellow]Not: 'choco' komutunun yüklü ve PATH'te olduğundan emin olun.[/yellow]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]İptal edildi.[/red]")
