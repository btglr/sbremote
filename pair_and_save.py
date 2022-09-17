import os
import re
import sys
import json
import time
import pyatv
import random
import asyncio
import inquirer
from yaspin import yaspin

pair = pyatv.pair
Protocol = pyatv.const.Protocol

config_dir = os.environ["CONFIG_DIR"]
output_filename = "appletv.json"
output_filepath = os.path.join(config_dir, output_filename)

async def scan(loop):
    with yaspin(text="Scanning") as sp:
        atvs = await pyatv.scan(loop)
    
    #print ("Scanning...", end="", flush=True)
    #print ("done", flush=True)

    print ("Select the number for the ATV to pair with:\n")
    ar = {}
    names = {}
    choices = []
    for atv in atvs:
        name = f"{atv.name} ({atv.address})"
        ar[name] = atv
        choices.append(name)
    
    questions = [ inquirer.List("atv", message="Select a device to pair with", choices=choices)]
    answers = inquirer.prompt(questions)
    
    name = answers['atv']
    atv = ar[name]
    
    print ("pairing atv %s" % (atv))
    pairing = await pair(atv, Protocol.AirPlay, loop)
    await pairing.begin()
    print ("Enter pairing code on screen")
    code = input ("Pairing code: ")
    pairing.pin(code)
    await pairing.finish()
    if pairing.has_paired:
        print("Paired with device!")
        print("Credentials:", pairing.service.credentials)
    else:
        print("Did not pair with device!")
    creds = pairing.service.credentials
    id = atv.identifier
    nj = {"credentials": creds, "identifier": id, "name": name}

    json.dump(nj, open(output_filepath, "w"))
    print (f"Saved credentials to {output_filepath}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scan(loop))
    loop.close()