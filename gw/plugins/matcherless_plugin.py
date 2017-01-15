import commands

@commands.command('sleep')
def sleep_command(data):
    return None

@commands.reactor('sleep')
def sleep_reactor(data):
    return None
