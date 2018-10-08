import libtcodpy as libtcod

def menu(con, header, options, width, screenWidth, screenHeight):
    if len(options) > 28: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate height of header (post auto-wrap) and one line per option
    headerHeight = libtcod.console_get_heigh_rect(con,0,0,width,
        screenHeight, header)

    # create off-screen console that reps the menu's window
    window = libtcod.console_new(width,height)

    # print header w/ auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window,0,0,width,height,
        libtcod.BKGND_NONE,libtcod.LEFT,header)

    # print options
    y = headerHeight
    letterIndex = ord('a')

    for optionText in options:
        text = '(' + chr(letterIndex) + ') ' + optionText
        libtcod.console_print_ex(window,0,y,libtcod.BKGND_NONE,
            libtcod.LEFT, text)

        y += 1
        letterIndex += 1

    # blit contents of window to root console
    x = int(screenWidth/2 - width/2)
    y = int(screenHeight/2 - height/2)

    libtcod.console_blit(window,0,0,width,height,0,x,y,1.0,0.7)

def inventoryMenu(con, header, inventory, inventoryWidth, screenWidth,
    screenHeight):
    # show a menu with each item of the inventory as an option
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']

    else:
        options = [item.name for item in inventory.items]

    menu(con,header,options,inventoryWidth,screenWidth,screenHeight)        
