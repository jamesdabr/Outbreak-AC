# First actual Blackwood visual session

Native3 actual build and independent verification passed D463/D464. Local1 failed sandbox socket startup, clean original reap/group closure; local2 started but release stdout buffering defeated readiness, clean exit0; both retained. Local3 used verified debug server under the same loopback permission, started native/map/gateway/HTTP and loaded the actual Wasm client in in-app browser.

OBSERVED: actual Blackwood greybox rendered; original model preload returned without fatal error; canvas gesture initialized audio. NOT OBSERVED: living character, successful connection, controllable movement or camera. Gateway admitted0 and exchanged zero datagrams. Pointer lock error WrongDocumentError. Screenshot files notes/previews/MAIN-local3-first-render.jpg and MAIN-local3-after-input.jpg are actual browser output, not gameplay acceptance.

Original launcher session86489 terminal947c58 exit0 CLOSED_VISUAL_SESSION,110.636s. Both owned children exited0/reaped/group_empty:true; gateway clean and all socket/timer handles closed. No active game service remains. D468 assigns World T274 real connection status and Engine T275 narrow source diagnosis. QA paused; full MVP incomplete.
