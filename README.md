# spoken_ide
## Calling a command 
* Commands are called using syntax: `chat (COMMAND)`

## Command Words
|  COMMAND |  |
|--------------|-------------------------------------------------------|
| Prompt  |  Initial command to write a function given a description, will populate in preview window |
| Add | Command designed to take input code block from preview window and modify it based on description |
| Test | Generates single printed test-case with spoken input as input parameters |
| Revise | Call to modify existing text in the preview window |
| Literal | Populates literal spoken input at cursor position |
| Run | Executes code in code editor window |
| Clear | Removes LLM discourse history for other commands |
| Up | Move cursor up |
| Down | Move cursor down |
| Left | Move cursor left |
| Right | Move cursor right |
| Save | Saves content in code editor window to local txt file |
| Load | Loads content from local txt file to preview window |
| Confirm / Submit | Publishes content from preview window to editor window |
| Undo | Restores text to previous state from last action, depth is 1 so will toggle if called successively|

