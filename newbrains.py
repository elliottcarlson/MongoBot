import sys
import os

if len(sys.argv) != 2:
    sys.exit("What do you want to call your new brainmeat?")

base = sys.argv[1]
cls = base.capitalize()
path = "brainmeats/" + base + ".py"

if os.path.isfile(path):
    sys.exit("command file already exists")

newfile = """from autonomic import axon, alias, help, Dendrite, Cerebellum, Synapse, Receptor

@Cerebellum
class {1}(Dendrite):

    def __init__(self, cortex):
        super({1}, self).__init__(cortex)

    # Example command function
    # The axon decorator adds it to the available chatroom commands,
    # based on the name of the function. The @help adds an entry to
    # the appropriate category.
    @axon
    @help("<I am an example>")
    def function_name(self):
        return

    # Example receptor method
    # The receptor decorator makes the defined method get autocalled
    # for any corresponding synapse. To see a list of available synapses
    # run tools/synapse.py or ask the bot for -synapse when running.
    @Receptor('heartbeat')
    def auto(self):
        return""".format(base, cls)


f = open(path, "w")
f.write(newfile)

sys.exit(base + ".py created in brainmeats")
