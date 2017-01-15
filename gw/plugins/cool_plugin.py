import commands, re

@commands.matcher(5)
def match_logic(data):
    name = data.name
    if re.match('cool_\d*', name):
        return 'tag1'
    else:
        return None
    
@commands.command('tag1')
def tag1_command(config):
    command_dict = config.args
    command_dict['command'] = 'tag1'
    return command_dict
    
@commands.reactor('tag1')
def tag1_reactor(data):
    coolness = data.coolness
    if int(coolness) > 5:
        return 'tag2'
    else:
        return None

@commands.command('tag2')
def tag2_command(config):
    command_dict = config.args
    command_dict['command'] = 'tag2'
    return command_dict

@commands.reactor('tag2')
def tag2_reactor(data):
    return None

