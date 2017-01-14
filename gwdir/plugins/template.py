import commands

@commands.matcher(2)
def match_logic(x):
    if x % 2 == 0:
        return 'tag1'
    else:
        return None

@commands.command('tag1')
def tag1_command(x):
    return "Command tag1={tag1}".format(tag1=x)
    
@commands.reactor('tag1')
def tag1_reactor(x):
    if x % 3 == 0:
        return 'tag2'
    else:
        return None

@commands.command('tag2')
def tag2_command(x):
    return "Command tag2={tag2}".format(tag2=x)

@commands.reactor('tag2')
def tag2_reactor(x):
    return None

