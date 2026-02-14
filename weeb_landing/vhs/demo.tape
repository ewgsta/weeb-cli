# VHS tape file for Weeb CLI demo
# This demonstrates the anime search and watch functionality

# Set up the terminal
Output demo.gif
Set Shell pwsh
Set FontSize 14
Set Width 1200
Set Height 700
Set Padding 20
Set Theme "Catppuccin Mocha"

# Type the command to start weeb-cli
Type "weeb-cli"
Sleep 500ms
Enter
Sleep 2s

# Navigate to search (assuming it's option 1 or 's')
Type "1"
Sleep 300ms
Enter
Sleep 1s

# Search for Angel Beats
Type "Angel Beats"
Sleep 500ms
Enter
Sleep 2s

# Select the first result
Type "1"
Sleep 300ms
Enter
Sleep 1.5s

# Choose to watch (assuming option 1)
Type "1"
Sleep 300ms
Enter
Sleep 1.5s

# Select episode 1
Type "1"
Sleep 300ms
Enter
Sleep 2s

# Show the stream selection screen
Sleep 2s

# Select first stream
Type "1"
Sleep 300ms
Enter
Sleep 1s

# Wait a bit to show the player starting message
Sleep 2s

# Exit gracefully (Ctrl+C)
Ctrl+C
Sleep 500ms

# Show final message
Sleep 1s
