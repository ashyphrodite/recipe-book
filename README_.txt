!! Run main.py as because it's the script file !!
All the other python files are used as libraries for organization purposes.
No need to manually create the save files. The program will automatically make them if they're missing. (checkFiles from misc)
Extract savefiles.zip to current directory (Extract Here) if you want some test data.

! Also, kindly run this on a terminal and not on an IDE. Thanks!

------------------------------------------------------------------
Only read this part if it interests you

Encryption Algorithm Description:
- First number on save files is the randomly generated shift (0-26) for caesar cypher.
- Letter characters are cyphered for both lowercase (a-z) and uppercase (a-Z) letters
- Number characters are cyphered using numbers (0-9) and dot (.).
- All the other characters are ignored and not cyphered.

The four dictionaries are stored in a list for convenient access to data.
Dictionaries data are only saved to files everytime you go back to Main Menu.
Hit Ctrl-C if you don't want an input to be saved.

-------------------------------------------------------------------------------
File                             blank        comment           code
-------------------------------------------------------------------------------
.\lib\recipe.py                    100             78            213
.\lib\supply.py                     62             49            135
.\lib\misc.py                       61             37            123
.\lib\supplier.py                   48             32             95
.\lib\log.py                        35             26             67
.\main.py                           22             23             44
-------------------------------------------------------------------------------
SUM:                               328            245            677
-------------------------------------------------------------------------------
Data grathered using cloc (Count Lines of Code): github.com/AlDanial/cloc


Program Outline
+--lib
|  +--recipe.py
|  |  > storeRecipes
|  |  > getRecipes
|  |  > addRecipe
|  |  > deleteRecipe
|  |  > deleteAllRecipes
|  |  > viewRecipe
|  |  > viewAllRecipes
|  |  > executeRecipe
|  |  > backToMain
|  |  > recipeBookMenu
|  |  > recipeBookLoop
|  |  
|  +--supply.py
|  |  > storeSupplies
|  |  > getSupplies
|  |  > addSupply
|  |  > deleteSupply
|  |  > deleteAllSupplies
|  |  > viewSupplies
|  |  > backToMain
|  |  > supplyMenu
|  |  > supplyLoop
|  | 
|  +--supplier.py
|  |  > storeSuppliers
|  |  > getSuppliers
|  |  > addSupplier
|  |  > deleteSupplier
|  |  > deleteAllSuppliers
|  |  > viewSuppliers
|  |  > backToMain
|  |  > supplyMenu
|  |  > supplyLoop
|  |
|  +--log.py
|  |  > storeLogs
|  |  > getLogs
|  |  > addLog
|  |  > viewLogs
|  |  > deleteLogs
|  |  > backToMain
|  |  > logsMenu
|  |  > logsLoop
|  |
|  `--misc.py
|     > checkFiles
|     > getData
|     > clearScreen
|     > changeColor
|     > printTitle
|     > printMenu
|     > getDateAndTime
|     > validInputLoop
|     > isPositiveInt
|     > isNonNegativeFloat
|     > charTypeAndInt
|     > typeAndIntToChar
|     > cypher
|     > decypher
|
+--savefiles
|  +--recipe.txt
|  +--supply.txt
|  +--supplier.txt
|  `--logs.txt
|
`--main.py
   > initialize
   > exitProgram
   > mainMenu
   > mainLoop
   > main <---- entry point