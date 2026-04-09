# Weeb CLI'a Katkıda Bulunmak

<div align="center">
  <a href="../../CONTRIBUTING.md">English</a> | <a href="CONTRIBUTING.md">Türkçe</a> | <a href="../de/CONTRIBUTING.md">Deutsch</a> | <a href="../pl/CONTRIBUTING.md">Polski</a>
</div>
<br>

Öncelikle, Weeb CLI'a katkıda bulunmayı düşündüğünüz için teşekkür ederiz! Yardımınız çok değerlidir.

Eğer anime izlemeyi, terminali ve pratik araçları seviyorsanız, doğru yerdesiniz.

## Başlarken

1. GitHub üzerinden depoyu **forklayın**.
2. Kendi fork'unuzu klonlayın:
   ```bash
   git clone https://github.com/ewgsta/weeb-cli.git
   cd weeb-cli
   ```
3. Bağımlılıkları geliştirici modunda kurun:
   ```bash
   pip install -e .
   ```

## İş Akışı

1. Özelliğiniz veya hata düzeltmeniz için yeni bir dal (branch) oluşturun:
   ```bash
   git checkout -b feature/ozellik-adiniz
   ```
2. Kod tabanında değişikliklerinizi yapın.
3. Değişikliklerinizi yerel olarak test etmek için `weeb-cli` komutunu çalıştırabilirsiniz; bu komut güncel çalışma alanınızı kullanacaktır.
4. Mümkünse test eklemeye çalışın. Testler `tests/` dizininde bulunur.
   ```bash
   pytest
   ```
5. Commit işlemini gerçekleştirin. Commit mesajlarınızın neyi değiştirdiğini net bir şekilde açıkladığından emin olun.
6. Forkunuza push yapın ve `main` dalına doğru bir Pull Request (PR) gönderin.

## Pull Request'ler

- Pull Request'lerinizi tek bir özelliğe, değişikliğe ya da hata düzeltmesine odaklı tutmaya çalışın. Bu, inceleme sürecini kolaylaştırır.
- Eğer ilgili bir `issue` (problem bildiriminiz) varsa, bakımcılara bağlam sağlamak için içeriğe ekleyin.
- Mevcut kod stiline uyun (Python kısımları için Black/Flake8).
- Eğer değişiklikleriniz uygulamanın dış davranışını etkiliyorsa, dökümantasyonları güncellediğinizden emin olun (`README.md`, `md/tr/README.md` vb.).

## Sorunlar (Issues)

Bir hata bulursanız veya bir öneriniz varsa, lütfen issue açmaktan çekinmeyin:
- Aynı konunun daha önce rapor edilip edilmediğinden emin olmak için **mevcut sorunları önceden arayın**.
- Bir hata bildirirken mümkün olduğunca fazla bağlam (detay) sağlayın. Olası detaylar: İşletim sistemi, Python sürümü ve Weeb CLI sürümü.
- Mümkün olan yerlerde hatanın tekrarlanabileceği adımları, log çıktılarını veya ekran görüntülerini ekleyin.

## Çeviriler ve Çoklu Dil Desteği (i18n)

Weeb CLI çoklu dil desteği barındırır (`en`, `tr`, `de`, `pl` vb.):
- Kullanıcı arayüzüne yeni bir metin ekleyen özelliklerin, `locales/` klasöründe bulunan tüm JSON dosyalarına (`en.json`, `tr.json`, `de.json`, `pl.json` vb.) eklemeler yapması gerekir.

---

Katkılarınız için tekrar teşekkür ederiz!
