# T060 SDK HTML minifier alias is also invoked by unchanged -O2 link

- Ticket: T060 revision 3.1 / D044; preparation only, no tool executed.
- Follow-up inspection: installed SDK `tools/link.py:2669` calls `minify_html` for HTML output; `minify_html` at line2623 calls `shared.get_npm_cmd('html-minifier-terser')`. `tools/shared.py:227` executes Node with `node_modules/.bin/<name>`.
- The installed `upstream/emscripten/node_modules/.bin/html-minifier-terser` is a symlink, outside D044's exact four bin aliases. The unchanged O2 HTML link therefore needs another explicit alias policy or remains blocked. No SDK rewrite, new flag, exception or tool execution performed.
- Proposed resolution: MAIN independently pin this exact internal alias chain/text/target under its appropriate confined root and amend the explicit alias decision, preserving every existing flag. All other aliases remain rejected. Current preparation can continue; future strict tool preflight remains fail closed until resolved.
