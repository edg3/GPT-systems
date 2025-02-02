"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
// in seach console at top (ctrl + p) type: `>debug st` (or F5) and select `Start Debugging`, it will open a debug window, then you can search for '>hello' and you should see Hello World, click on it and see the error
const vscode = __importStar(require("vscode"));
const url = "http://127.0.0.1:11434/api/generate";
const headers = { "Content-Type": "application/json" };
function activate(context) {
    console.log('Congratulations, your extension "edg3-ext" is now active!');
    const disposable = vscode.commands.registerCommand('edg3-ext.deepseek', () => {
        vscode.commands.executeCommand('edg3-ext.panel');
    });
    context.subscriptions.push(disposable);
    // query
    async function postData(url, payload) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            if (response.status !== 200) {
                const errorBody = await response.text();
                throw new Error(`HTTP error! status: ${response.status} - ${errorBody}`);
            }
            let body = await response.text();
            return JSON.parse(body);
        }
        catch (error) {
            console.error('Error posting data:', error);
            return error;
        }
    }
    // create panel
    const disposablePanel = vscode.commands.registerCommand('edg3-ext.panel', () => {
        const panel = vscode.window.createWebviewPanel('deepseekChat', 'Deepseek Chat', vscode.ViewColumn.One, { enableScripts: true });
        panel.webview.html = getWebviewContent();
        panel.webview.onDidReceiveMessage(async (message) => {
            if (message.command === 'chat') {
                let payload = { model: 'deepseek-r1:8b', prompt: message.text, stream: false };
                try {
                    const data = await postData(url, payload);
                    let responseText = data.response;
                    panel.webview.postMessage({ command: 'chatResponse', text: responseText });
                }
                catch (error) {
                    console.error('Error:', error, 'for payload:', payload, 'and url:', url);
                    panel.webview.postMessage({ command: 'chatResponse', text: 'Error: ' + error });
                }
            }
        });
    });
    context.subscriptions.push(disposablePanel);
}
function getWebviewContent() {
    // use extention `es6-string-html` and out the /*html*/ comment at string start to get full syntax hilighting
    return /*html*/ `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Deepseek Chat</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 1rem; }
            #prompt { width: 100%; box-sizing: border-box; padding: 0.5rem; height: 3rem; }
            #response { border: 1px solid #ccc; margin-top: 1rem; padding: 0.5rem; min-height: 200px; margin: 12px; }
            button {
                background-color: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
                border: none;
                padding: 0.5rem 1rem;
                cursor: pointer;
                font-size: 1rem;
                border-radius: 3px;
            }
            button:hover {
                background-color: var(--vscode-button-hoverBackground);
            }
        </style>
    </head>
    <body>
        <h2>Deepseek Chat</h2>
        <textarea id="prompt" rows="3" placeholder="Ask something from Deepseek R1 8b here..."></textarea><br>
        <button id="askBtn">Ask</button><br>
        <div id="response"></div>
        <div id="thinking"></div>
        <script>
            const vscode = acquireVsCodeApi();
            document.getElementById('askBtn').addEventListener('click', () => {
                const text = document.getElementById('prompt').value;
                vscode.postMessage({ command: 'chat', text });
            });
            window.addEventListener('message', event => {
                const { command, text } = event.data;
                if (command === 'chatResponse') {
                    let splt = text.split('</think>');
                    splt[0] = splt[0].replace(/<think>/g, '<span style="color: #ccc; font-style: italic;">') + '</span>';
                    document.getElementById('thinking').innerHTML = splt[0];
                    document.getElementById('response').innerHTML = marked.parse(splt[1].trim());
                }
            });
        </script>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    </body>
    </html>`;
}
function deactivate() { }
//# sourceMappingURL=extension.js.map