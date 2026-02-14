# VHS tape - Weeb CLI Search Demo
# Demonstrates searching for Angel Beats anime

Output demo-search.gif
Set Shell pwsh
Set FontSize 16
Set Width 1400
Set Height 800
Set Padding 25
Set Theme "Dracula"
Set TypingSpeed 100ms

# Start the application
Type "weeb-cli"
Sleep 500ms
Enter
Sleep 2.5s

# Go to search
Type "1"
Enter
Sleep 1.5s

# Type search query slowly for effect
Type@500ms "Angel Beats"
Sleep 800ms
Enter
Sleep 3s

# Show results by waiting
Sleep 2s

# Navigate through results
Down
Sleep 500ms
Down
Sleep 500ms
Up
Sleep 500ms

# Select first result
Enter
Sleep 2s

# Show anime details screen
Sleep 3s

# Exit
Ctrl+C
Sleep 500ms
Ctrl+C
