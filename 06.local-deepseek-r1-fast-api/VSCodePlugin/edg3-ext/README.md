# edg3-ext README

Using ```Ollama``` to run ```Deepseek R1 8b``` locally on Windows 11, via WSL2, this extension runs API requests through the instance you run, and shows in a simple clean manner inside VSCode.

Usage when installed:
- ```ctrl + p``` and type ```>deep``` to see ```>Deepseek``` listed.

## Features

Takes a message you input and send it to Deepseek, in Ollama, then gives the full response when the API request is complete.

## Requirements

A computer that can run its on instance of an LLM, through Ollama. It's advisable as is to have a graphics card that can run large models (at time of production using NVIDIA GeForce RTX 3050 OC 8Gb; and long responses average 2 minutes for details requested through query, see prompt guides for an idea to get the best answers).

You can use the smaller models of Deepseek, just change the ```8b``` to ```1.5b```, or ```7b```, as you need. If you can't get it to run, always just move to ```1.5b``` for starting to try it out.

## Known Issues

The button doesn't disable when you send a query to the API.

## Release Notes
### 0.0.1

Initial release of an extension to bring a little faster, prettier, method to ask Deepseek R1 queries through VSCode while working there.

---

The extension is kept clean and minimal, only adding a Panel openable with the ```ctrl + p``` search to be unintrusive and simple enough to understand/use.

* [Extension Guidelines](https://code.visualstudio.com/api/references/extension-guidelines)

**Enjoy!**
