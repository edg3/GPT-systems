# Local Deepseek R1: Fast API
---
- **Goal:** Get a small Deepseek model running through Ollama.

- **Requirements:** 
  - Windows 11
  - WSL2
  - Ollama
  - Deepseek R1 model

## Disclaimer:
Anyone using these steps is responsible for their own machine and I cannot be held liable. This guide is provided under a CC0 license, and all packages are licensed by their own licenses from where they were retrieved.

## Steps:

1. I use WSL2 in Win11
2. ```curl -fsSL https://ollama.com/install.sh | sh```
3. Run deepseek-r1 with the version you want and your system can handle (1.5b, 7b, 8b, 14b, 32b, 70b, 671b) - recommended: first start with 1.5b to see how it all works with ease

Source: https://ollama.com/library/deepseek-r1

```ollama pull deepseek-r1:8b```

4. Verify ollama sees it after:

```ollama list```

You should see something along the lines of: ```deepseek-r1:8b    28f8fd6cdc67    4.9 GB    13 seconds ago```

5. ```ollama serve```

***Note, Discord uses port 11434, so you might need to use*** ```export OLLAMA_HOST=127.0.0.1:11435```

6. In another terminal open **WSL** as well, and run ```ollama run deepseek-r1:8b``` **swap 8b for the model you chose**

You can then run your first query and it will first give you its **think** step; then the answer:

Question: ```As an expert in Godot 4.3, how can I animate 3D characters I have rendered into the scene?```

Think:
```
<think>
Okay, so I'm trying to figure out how to animate a 3D character in Godot 4.3 that I've already
rendered into the scene. I remember seeing some tutorials but I'm not entirely sure about the
exact steps. Let me try to break this down.

First, I think I need to have my character model ready. But wait, if it's already rendered, does
that mean it's in a separate file? Or is it part of the scene now? Maybe I should check where it
is. If it's in the scene as a node, then perhaps I can work on its animations without moving it.

Next, I remember something about animation nodes in Godot. There's probably a way to create
these nodes for each action my character needs to perform. So, if my character has multiple
actions like walking or jumping, each would have its own animation node. That makes sense
because it allows me to play different animations based on what the character is doing.

I think I need to use the Character Animation Controller (CAC) as mentioned. How do I set that
up? I guess I import a specific script from the GD Library. Oh right, it's
'CharacterAnimationController.gd'. Then, I can add it to my scene and set it as the controller
for my character node.

Now, how do I create an animation node? There should be a button in the Dopesheet called 'Create
Animation Node', which creates a node that controls how the animations are played. Each of these
nodes will have properties like 'Main Animation' which is the core movement, and then other
animations for specific actions like falling or jumping.

I'm a bit confused about creating an animation from a blend file. Do I need to import it first?
Or does Godot handle it automatically when I assign the CAC? Maybe I should make sure that my
blend file is in a format that Godot supports, like .blend or something else. Oh wait, no, in
Godot, you can directly reference the blend file in the animation node's 'Main Animation'
property. So I just need to point it to the correct file.

Assigning animations to states sounds important. Each state like 'walk', 'run', and 'fall' will
trigger specific animations. So when the character is moving, the 'walk' state's main animation
plays. When it jumps, 'jump' state takes over with its own animation.

What about transitions? How do I make the character switch between states smoothly? I think
there's a transition window where I can set up keyframes to change from one state to another at
certain times. This is probably where I can animate the transition, like a jump animation
starting and then switching to a fall or something else.

I remember that blend trees are used for mixing animations. For example, if my character is both
walking and jumping, the blend tree can mix those two movements smoothly so it looks natural.
That means setting up nodes with different blending percentages based on how much each animation
contributes at any given time.

Testing is crucial. I should play around with the states and transitions to see how the
animations look together. Maybe create a simple scene where the character walks, jumps, falls,
and then plays the combined animations to check for any issues or gaps in the movement.

Optimizing performance might be a concern if there are many animations playing at once. I think
Godot handles this well, but it's something to keep an eye on, especially with more complex
scenes.

Finally, when everything looks good, I can integrate this into my game by dragging and dropping
the animation nodes into the scene tree. This way, the CAC can manage all the animations for the
character seamlessly.

I'm not entirely sure if I missed any steps or got a detail wrong. Maybe I should look up some
Godot documentation on the Character Animation Controller to make sure I'm setting it up
correctly. Also, experimenting with different states and transitions might take some time, but
that's part of the learning process.
</think>
```

Answer:
```
To animate a 3D character in Godot 4.3, follow these organized steps:

1. **Character Model Preparation**:
   - Ensure your character model is ready and in a supported format (e.g., .blend or other). If rendered into the scene, it can be accessed as a node.

2. **Importing and Setting Up the Character Animation Controller (CAC)**:
   - Import `CharacterAnimationController.gd` from the GD Library.
   - Add the CAC to your scene and set it as the controller for your character node in theSceneTree.

3. **Creating Animation Nodes**:
   - In the Dopesheet, click the "Create Animation Node" button to create a new animation node.
   - Use the node properties to assign 'Main Animation' (from your blend file) and other specific animations for actions like walking or jumping.

4. **Assigning Animations to States**:
   - Create states in CAC (e.g., 'walk', 'jump') and assign corresponding animations for each state.

5. **Setting Up Transitions Between States**:
   - Use the Transition window to create keyframes that trigger state changes, ensuring smooth transitions between animations.

6. **Blending Animations with Blend Trees**:
   - For complex actions (like walking while jumping), set up blend trees in CAC to mix animations smoothly, adjusting blending percentages as needed.

7. **Testing and Debugging**:
   - Playtest the character in a simple scene to assess animation flow and identify any gaps or issues.

8. **Optimizing Performance**:
   - Monitor performance, especially with multiple animations, leveraging Godot's optimizations for smooth operation.

9. **Integrating into Your Scene**:
   - Drag and drop animation nodes into your scene tree, allowing CAC to manage all character animations seamlessly.

By following these steps, you can create and integrate detailed 3D character animations into your Godot project effectively.
```

7. We need to still have ollama running, but you can use ```OLLAMA_HOST=127.0.0.1:11435 ollama serve``` and ```ollama run deepseek-r1:8b``` to run them it. **Note: I do get inconsistency in my local for the ports despite specifying 11435, unsure about that thought.**

8. You can use curl to make an API call:

```
curl http://localhost:11434/api/generate -d '{
  "model": "deepseek-r1:8b",
  "prompt": "Why is the sky blue?"
}'
```
Add the following to your *<windows_user_profile>/.wslconfig* (create if not there):

```
[wsl2]
networkingMode=mirrored

```

```wsl --shutdown``` from command prompt then ```wsl``` to restart it.

9. Running the paython script in Win11 after sorting 11, it gave the start of the response:

```
PS D:\...> python .\client-request.py
Q:  As an expert in Godot 4.3 C#, please give me a lesson on how to create a simple 2D proceduraly generated world using my own implemented seeded perlin noise instead of built in noise.
Sending request
Response received
Execution time: 218.64354467391968 seconds
<think>
Okay, so I'm trying to figure out how to create a simple 2D procedurally generated world using my own implemented seeded Perlin noise instead of the built-in noise functions in Godot 4.3 with C#. ...
```

10. Using the steps shared in ```client-request.cs``` in the same directory, and using copilot to convert the pythony code to C#: and clean up, received the response:

```
PS D:\...> dotnet run
Q: As an expert in Godot 4.3 C#, please give me a lesson on how to create a simple 2D procedurally generated world using my own implemented seeded perlin noise instead of built in noise.
Sending request
Response received
Execution time: 107,2315056 seconds
<think>
Okay, so I want to create a simple 2D procedurally generated world using my own seeded Perlin noise in Godot 4.3 with C#. ...
```

11. To generate a VSCode plugin that uses this API in windows, in a folder, and you can stick with the default values:

```shell
npx --package yo --package generator-code -- yo code
```

I won't give steps as a tutorial; but you can see how the model running using step 11 can answer me inside VSCode in a readable format in the editor itself. Note that it needs decent explanations and context, and it's adjusted so the thinking process shows after the result.

12. Build the VSCode extension
- cd <your-extension-folder>
- npm install -g vsce
- vsce package

***if npm install gives issues as vsce wont install: npx @vscode/vsce package***

This will generate a .vsix file which you can install in VSCode
To install the extension, open VSCode and go to the Extensions view.
Click on the ellipsis (...) in the top right corner and select "Install from VSIX..."
Then select the generated .vsix file.

13. To add it after you have built it on your own install of VSCode, ```ctrl + p``` and type ```>extensions``` to see ```Extensions: Install from VSIX...``` listed.