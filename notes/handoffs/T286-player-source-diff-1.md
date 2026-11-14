# T286 source diff

Readback verifies reversing only this block restores the exact starting file SHA256; T285 weapon mapping preserved.

```diff
--- T286-start/source/src/rendermodel.cpp
+++ T286-source/source/src/rendermodel.cpp
@@ -1106,7 +1106,18 @@
     loopv(players) if((d = players[i]) && d->state!=CS_SPAWNING && d->state!=CS_SPECTATE && (!player1->isspectating() || player1->spectatemode != SM_FOLLOW1ST || player1->followplayercn != i)) renderclientp(d);
     bool localbody = player1->state==CS_DEAD || ((reflecting && !refracting) && (player1->state!=CS_SPECTATE || player1->spectatemode==SM_FLY));
 #if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
-    localbody = localbody || outbreakthirdperson();
+    if(outbreakthirdperson())
+    {
+        // Camera collision can leave the view inside the local body. Use the real
+        // body/camera bounds, including current crouch height, without moving either.
+        vec offset(camera1->o);
+        offset.sub(player1->o);
+        const float clearance = player1->radius + camera1->radius;
+        const bool overlapping = offset.sqrxy() <= clearance*clearance &&
+            offset.z >= -player1->eyeheight - camera1->aboveeye &&
+            offset.z <= player1->aboveeye + camera1->eyeheight;
+        localbody = !overlapping; // Recomputed each draw: restore once clear.
+    }
 #endif
     if(localbody) renderclientp(player1); // one local draw, including overlapping reflection cases
 }
```
