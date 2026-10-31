# LH_HideMe – Project knowledge and working rules

## Starting future sessions

- Read AGENTS.md, README.md, LH_HideMe.toc, and LH_HideMe.lua first.
- Check Git status, remotes, and recent commits before making changes.
- Current code and Git state take precedence over outdated information here.
- Communicate with the user in German. All addon messages, comments, metadata, and project documentation must be in English, as requested by the user on October 11, 2026.
- Work on LH_HideMe. Other addons in the parent directory are separate projects.
- Keep this file up to date when making relevant changes.
- The Forever branch keeps interface 16001. Version 0.20.1 adds independent MainActionBar EndCaps/BorderArt hiding and limits chat-tab hiding to General and Combat Log; whisper tabs follow Blizzard. Classic bag/micro button discovery remains TBC-only. .settings-test.py passes the Forever artwork and combat checks. Live in-game verification is pending.

## Project and repository

- Small Lua addon for the WoW Forever Beta.
- Folder: C:\Program Files (x86)\World of Warcraft\_classic_beta_\Interface\AddOns\LH_HideMe
- Public repository: https://github.com/ekimmerst/LH_HideMe
- Remote origin: https://github.com/ekimmerst/LH_HideMe.git
- Branch: main, tracking origin/main. Local commit history is preserved.
- As of October 21, 2026: version 0.20.0; interface version 16001.
- Last verified commit before the 0.15.0 publication: 77e5927 (Simplify README for addon users).
- The user successfully published the addon previously.
- Requires LH_Tweaks as the shared configuration host; no build step.

## Files

- LH_HideMe.toc: metadata, version, interface version, and Lua load order.
- LH_HideMe.lua: visibility implementation and shared settings getters. Settings.lua: native settings subpage.
- Media/Icon.tga: 256x256 uncompressed 32-bit LH addon-list texture identical to LH_Tweaks/Icon.tga, referenced by IconTexture in LH_HideMe.toc.
- Media/Icon.png: original generated artwork.
- README.md: concise English addon-page description, commands, installation, and a final Changelog section covering all commits from a player's perspective (user request on October 15, 2026). Keep it focused on players, in the style of a CurseForge listing; omit implementation details and test reports. Keep the changelog updated for future changes.
- AGENTS.md: information for future work.

## Commands

Configured through Settings > AddOns > LH Tweaks > LH HideMe, or through the chat commands below.

- /lh_hideme all on: set all supported hiding settings to on.
- /lh_hideme all off: set all supported hiding settings to off.
- /lh_hideme addons-icon on: hide the minimap addon compartment button.
- /lh_hideme addons-icon off: show the minimap addon compartment button.
- /lh_hideme bag-bar on: hide the bag bar.
- /lh_hideme bag-bar off: show the bag bar.
- /lh_hideme calendar-icon on: hide the minimap calendar button.
- /lh_hideme calendar-icon off: show the minimap calendar button.
- /lh_hideme chat-bar on: hide inactive chat input; press Return to start typing.
- /lh_hideme chat-bar off: keep the General input visible without taking keyboard focus.
- /lh_hideme chat-buttons on: hide standard chat buttons in all chat windows.
- /lh_hideme chat-buttons off: show standard chat buttons.
- /lh_hideme chat-tabs on: hide all standard chat tabs, including General and Combat Log.
- /lh_hideme chat-tabs off: show only the General tab (ChatFrame1); all other tabs remain hidden.
- /lh_hideme day-night-indicator on: hide the minimap day-night indicator.
- /lh_hideme day-night-indicator off: show the minimap day-night indicator.
- /lh_hideme exp-bar on: permanently hide the entire status-bar area and borders.
- /lh_hideme exp-bar off: always show the available status-bar area and borders.
- /lh_hideme fishing-bobber-tooltip on: hide the fishing bobber tooltip.
- /lh_hideme fishing-bobber-tooltip off: allow normal mouseover tooltips again.
- /lh_hideme micro-menu on: hide the micro menu.
- /lh_hideme micro-menu off: show the micro menu.
- /lh_hideme player-frame on: show the player frame with a target, in combat, or below full health.
- /lh_hideme player-frame off: always show the player frame.
- /lh_hideme toolbars on: show active standard action bars only with a target or in combat.
- /lh_hideme toolbars off: always show active standard action bars.
- /lh_hideme targetauras on: hide buffs and debuffs on the standard target frame.
- /lh_hideme targetauras off: restore available target buffs and debuffs.
- /lh_hideme except toolbar <1-8>: add a health visibility exception for this action bar while toolbar hiding is on.
- /lh_hideme except toolbar <1-8> off: remove that exception. Multiple exceptions are supported and retained by all on/off.
- /lh_hideme help: show all commands and usage.
- /lh_hideme without parameters: show help.
- /lh_hideme status: show all hiding settings.

on enables hiding; off disables it.
Commands are case-insensitive; leading and trailing whitespace is removed.
Invalid commands do not change settings and refer the user to help.

Status lists all targets alphabetically with the parameter name, English label,
and saved on/off state. Pending changes are marked. Status displays settings;
it does not measure actual visibility when other addons interfere.

## Rename to LH_HideMe

- Version 0.19.2 renames the folder, TOC, Lua file, title, icon path, chat prefix, slash registration and saved-variable table to LH_HideMe.
- Use /lh_hideme; the saved-variable table is LH_HideMeDB. Individual setting keys remain unchanged.
- WoW does not automatically load the old HideMe saved-variable file for the renamed addon. The README documents manual migration with WoW closed. Without migration, hiding options start disabled.
- Restart WoW after the folder rename. In-game verification of the rename remains pending.

## Technical implementation

- Version 0.19.1 installs chat-tab guards when LH_HideMe's saved variables load, before login chat setup finishes. OnShow catches native SetShown paths in addition to the existing Show hook; a guarded SetAlpha hook keeps hidden tabs transparent during subsequent fades, including combat. The applied tab mode is retained until combat-deferred changes take effect. Off restores General's alpha and visibility while other tabs remain hidden. Existing 0.19.0 working-tree changes were preserved.

- Version 0.19.0 includes MultiCastActionBarFrame in toolbars. The Forever source defines its action pages, selection flyout, summon and recall controls as children in Blizzard_ActionBar/Shared/MultiCastActionBarFrame.xml. The existing alpha-only target/combat handling, combat-deferred settings and late-addon discovery apply. TotemFrame is a separate player-frame duration display and is not an action bar. Health exceptions remain limited to action bars 1–8. In-game verification is pending.

- fishing-bobber-tooltip: LH_HideMeDB.hideFishingBobberTooltip. GameTooltip OnShow/OnUpdate hooks inspect the first line only for UIParent-owned world tooltips; secret text is skipped. Matches English Fishing Bobber, German Angelschwimmer, or FISHING_BOBBER if provided by the client. Other locales without that global are not yet supported. Mode changes and hook installation defer in combat; installed hooks enforce the applied mode. Off relies on the next normal mouseover and never forces stale tooltip content to show. Included in all/help/status and per-character persistence. The user confirmed basic functionality in game on October 16, 2026 with version 0.18.0; the full combat/persistence compatibility matrix remains pending.

- day-night-indicator: LH_HideMeDB.hideDayNightIndicator; MinimapCluster.DielFrame, discovered through GetTargetFrames. Confirmed in the forever branch's Blizzard_Minimap/Camelot/Diel.lua, where the frame contains both the cycle background and border. Uses generic Show/Hide and Show/SetShown enforcement, combat deferral, missing-frame retry and per-character persistence. Independent of GameTimeFrame and the minimap itself. Included automatically in all and status. The user confirmed on October 16, 2026 that version 0.17.0 works in game; the full combat/persistence compatibility matrix remains pending.
- The user confirmed on October 15, 2026 that targetauras works in game with version 0.16.2. This supersedes earlier pending basic-functionality notes; the full combat/persistence compatibility matrix remains pending.
- targets defines the setting key, label, and frames for each parameter.
- Versions 0.16.0 and 0.16.1 both failed in game. Their tests modeled older Classic named buttons/pools, not Forever. Version 0.16.2 uses TargetFrame.TargetFrameContent.TargetFrameContentContextual.Auras, the shared buff/debuff container returned by GetAuraContainer in the forever branch of Gethe/wow-ui-source (Interface/AddOns/Blizzard_UnitFrame/Mainline/TargetFrame.lua; Camelot/TargetFrame.lua uses OnLoadBase). This source branch is required for future Forever API research. Container alpha hides later children automatically; Show/SetAlpha enforcement and ConfigureAuraContainer post-hook retain hiding across updates. Legacy paths remain as fallbacks. Discovery now reports pending if no aura display was found instead of treating the mere existence of TargetFrame as success. In-game confirmation remains pending.
- Version 0.16.0 did not hide the user's buffs when targeting themselves in game. Version 0.16.1 adds the missing TargetFrame.UpdateAuras post-hook used by Classic to discover buttons created after LH_HideMe's target/aura event runs. UpdateAuras and UpdateAuraFrames hooks are tracked independently per frame. In-game confirmation of this fix remains pending.
- targetauras: LH_HideMeDB.hideTargetAuras. Alpha-only gating of TargetFrameBuffN/TargetFrameDebuffN and active TargetFrame.auraPools frames. Never reads aura data or calls Show/Hide on aura buttons. Show/guarded SetAlpha hooks enforce the applied mode; legacy TargetFrame_UpdateAuras and modern UpdateAuraFrames hooks discover newly created buttons. UNIT_AURA for target, target changes and addon loading retry discovery. Mode changes and hook installation defer in combat. Previously discovered pooled buttons are also restored with off. Transparent buttons may retain mouse input. In-game verification is pending.
- all is a bulk slash command, not a target or saved setting. Validates on/off first, writes all targets' settings before invoking ApplyTargets once, and reports combat or missing-frame pending changes. Includes future targets automatically. Individual commands remain usable afterward. Preserves target-specific off behavior and permanent Combat Log hiding.
- addons-icon: LH_HideMeDB.hideAddonsIcon; AddonCompartmentFrame. Uses generic Show/Hide, Show enforcement, per-character persistence, missing-frame retry and combat deferral. Does not disable addons or remove their menu registrations.
- calendar-icon: LH_HideMeDB.hideCalendarIcon; GameTimeFrame. Uses the generic Show/Hide implementation, Show enforcement, per-character persistence, missing-frame retry and combat deferral. Hiding the parent also hides calendar invitation textures; the calendar feature remains available through other entry points.
- Version 0.10.1 renames the mistaken char-bar command to chat-bar everywhere, retaining LH_HideMeDB.hideChatInput. No old-command alias is exposed. HideCombatLog always gates ChatFrame2, ChatFrame2Tab, ChatFrame2EditBox, ChatFrame2ButtonFrame and CombatLogQuickButtonFrame_Custom independently of settings. Show and guarded SetAlpha hooks enforce zero opacity during combat; direct hiding and hook installation wait until outside combat. Selected Combat Log returns to General via FCF_SelectDockFrame when available. Events, application and new-window hooks retry discovery. Combat-log messages and subscriptions are not cleared.
- chat-bar: LH_HideMeDB.hideChatInput. GetTargetFrames discovers ChatFrameNEditBox and chat.editBox using standard/temporary chat discovery. ApplyChatInput preserves focused fields; on hides inactive inputs and hides them on focus loss. Off shows only the primary General input when idle and restores it through a Hide hook. No Show hook hides inputs, because Blizzard shows them before setting focus. Never calls SetFocus or replaces input scripts; HookScript preserves existing handlers. Combat changes and hook installation are deferred. New-window hooks and chat/addon events include this target.
- bag-bar: LH_HideMeDB.hideBagBar; frame BagsBar.
- micro-menu: LH_HideMeDB.hideMicroMenu; frames MicroMenuContainer and MicroMenu, if available.
- chat-buttons: LH_HideMeDB.hideChatButtons. GetTargetFrames resolves available ChatFrameMenuButton, ChatFrameChannelButton, QuickJoinToastButton, voice mute/deafen buttons, and button panels/scrollbars/scroll-to-bottom/minimize controls for NUM_CHAT_WINDOWS and CHAT_FRAMES (including temporary windows). Frame references are deduplicated. Uses the existing Show/Hide hooks and combat deferral. UPDATE_CHAT_WINDOWS, UPDATE_FLOATING_CHAT_WINDOWS, later ADDON_LOADED and guarded one-time FCF_OpenNewWindow/FCF_OpenTemporaryWindow hooks discover new controls. Chat text, tabs and edit boxes are not targeted; third-party buttons are not covered.
- LH_HideMeDB is saved per character through SavedVariablesPerCharacter.
- chat-tabs: LH_HideMeDB.hideChatTabs. GetTargetFrames resolves ChatFrameNTab and chat.tab for NUM_CHAT_WINDOWS and CHAT_FRAMES, sharing discovery events and new/temporary-window hooks with chat-buttons. References are deduplicated. Uses existing Show hooks and combat deferral. On hides every tab; off shows only ChatFrame1Tab (falling back to ChatFrame1.tab), regardless of its localized or renamed title. Other tabs remain hidden in both modes, including the default off setting. Independent of chat-buttons; text/edit frames are not targeted. The user requested this behavior after version 0.9.0 off revealed Voice and unused Chat 6/7 tabs.
- exp-bar: LH_HideMeDB.hideExpBar. Gates StatusTrackingBarManager alpha, including borders and all XP/reputation/other contents. Legacy fallback frames: MainMenuExpBar, ReputationWatchBar, MainMenuBarMaxLevelBar. Version 0.14.0 permanently sets alpha to zero with on and restores alpha to one with off. Removes the two-second display timer, deadline and PLAYER_XP_UPDATE/PLAYER_LEVEL_UP registrations. Show and guarded SetAlpha hooks enforce hiding without recursion, including during combat. Mode changes and hook installation defer in combat. Later ADDON_LOADED retries discovery. Transparent frames may retain mouse input.
- toolbars: LH_HideMeDB.hideToolbars. MainActionBar, MultiBarBottomLeft, MultiBarBottomRight, MultiBarRight, MultiBarLeft, MultiBar5/6/7, PetActionBar, StanceBar, PossessActionBar and OverrideActionBar, when available. ApplyToolbars changes alpha only, preserving Blizzard's activation/paging/special-state visibility; it never calls Show/Hide or replaces their state drivers. Transparent bars retain key bindings and may receive mouse input. Third-party bars are not covered.
- Toolbar alpha updates on target and combat changes; Show hooks restore the current alpha. Hook setup and applied-mode changes wait until out of combat, while alpha can update in combat. Later ADDON_LOADED events retry optional toolbar discovery. Inactive bars remain inactive with off.
- Version 0.15.0 adds LH_HideMeDB.toolbarExceptions, normalized to eight boolean entries per character. Numbers 1–8 map to MainActionBar, MultiBarBottomLeft, MultiBarBottomRight, MultiBarRight, MultiBarLeft, MultiBar5, MultiBar6 and MultiBar7 (game settings numbering, not action pages). Selected bars use the same health curve as PlayerFrame while hideToolbars is enabled; target/combat still force alpha 1. Without curve support they retain target/combat behavior. No Show/Hide calls or visibility drivers are added. Applied exceptions are copied outside combat so mode changes defer consistently. Player UNIT_HEALTH/UNIT_MAXHEALTH now update toolbar alpha too. Help/status expose exceptions; all on/off preserves them.
- player-frame: LH_HideMeDB.hidePlayerFrame; frame PlayerFrame. With curve support, the frame stays shown and health controls alpha via UnitHealthPercent("player", false, healthAlphaCurve). A Step curve maps fraction 0 to alpha 1 and fraction 1 to alpha 0. The result is passed directly to SetAlpha, never compared or inspected. Mana is not queried. Transparent frames may remain interactive.
- Version 0.5.0 failed in game with a secret-number comparison in PlayerNeedsFrame. Version 0.5.1 guarded secret values but kept the frame always visible on the user's client. The user approved removing health/mana conditions temporarily for version 0.5.2; do not restore them without discussing the client restrictions.
- RegisterStateDriver keeps the player frame shown with curve support. Clients without the required APIs retain the version 0.5.2 target/combat visibility driver. Registration and direct Show/Hide calls occur only outside combat.
- PLAYER_TARGET_CHANGED, PLAYER_REGEN_DISABLED, UNIT_HEALTH and UNIT_MAXHEALTH update player alpha; PLAYER_REGEN_ENABLED applies pending settings and reevaluates. target.appliedHiding preserves the applied mode until deferred combat changes can be applied. Target/combat/off set alpha to 1.
- Settings persist across /reload and game restarts.
- Saved values are normalized to booleans.
- Hiding is disabled by default.
- ApplyTarget applies visibility.
- ApplyTargets processes all targets or only pending targets.
- InCombatLockdown prevents Show/Hide calls and hook setup during combat.
- target.pending tracks pending changes.
- PLAYER_REGEN_ENABLED applies changes after combat ends.
- Missing frames result in pending changes; later ADDON_LOADED events retry application.
- PLAYER_LOGIN and PLAYER_ENTERING_WORLD apply all settings.
- A hooksecurefunc hook on Show hides frames again when hiding is enabled.
- hookedFrames prevents duplicate hooks.
- Hooks check the current setting so that off continues to work.
- Other addons can affect the same frames.

## Changes and verification

- Version 0.19.1 passed Lua 5.1 simulations for saved on/off login, native-style SetShown bypassing Show, Show and alpha enforcement, combat-deferred on/off, General alpha restoration, other tabs remaining hidden, late tabs and all on/off. Existing totem-toolbar and permanent status-bar simulations and git diff --check passed. The user confirmed on October 21, 2026 that the login fix works in game; the full combat/persistence compatibility matrix remains pending.

- Version 0.19.0 passed Lua 5.1 simulations for totem toolbar on/off, saved-only startup, target/combat transitions, combat-deferred settings, Show enforcement, late loading, absent class bars, inactive-bar preservation, invalid commands and all on/off. Existing permanent status-bar regression simulations and git diff --check passed. In-game verification is pending.

- Version 0.18.0 passed Lua 5.1 simulations for fishing-bobber-tooltip default/saved startup, late loading, English/German/client-global names, unrelated tooltips, secret text, OnShow/OnUpdate, combat-deferred modes, invalid commands, all on/off, help and status. Day-night-indicator and permanent status-bar regressions passed. The user subsequently confirmed basic functionality in game on October 16, 2026. The full combat/persistence compatibility matrix remains pending.

- Version 0.17.0 passed Lua 5.1 simulations for day-night-indicator default/saved startup, on/off, Show/SetShown enforcement, combat-deferred changes, invalid commands, late-frame discovery, all on/off, help/status and independence from the calendar and minimap. Existing status-bar regressions and git diff --check passed. The user subsequently confirmed basic functionality in game on October 16, 2026. The full combat/persistence compatibility matrix remains pending.
- Add new targets to targets, help, and README.
- Status uses targets automatically.
- Preserve existing setting keys and the meaning of on/off.
- Update the version in LH_HideMe.toc and README for functional releases.
- Change the interface version only when supported by evidence.
- The user confirmed on October 11, 2026 that version 0.5.2 player-frame hiding and version 0.5.3 health-based visibility work in game. The full test matrix remains pending.
- Lua, LuaJIT, and luac were unavailable in the previous agent environment.
- Version 0.5.0 was checked for syntax and simulated WoW state changes using a temporary Lupa Lua 5.1 runtime (target, health/mana, combat, deferred mode changes, missing frames, and existing targets). This does not replace an in-game test.
- Version 0.5.1 passed the existing Lua 5.1 state simulations and regression simulations using comparison-rejecting sentinel values for each of the four resource APIs, including Show hooks, events, on/off, recovery to readable values, target short-circuiting, and clients without issecretvalue. Actual WoW secret values cannot be reproduced by Lupa; in-game verification remains required.
- Version 0.5.2 passed Lua 5.1 syntax and simulated target/combat transitions, enabling with an existing target, Show hooks, deferred on/off changes, invalid commands, other targets, missing-frame retry, and saved-setting reapplication. Resource API stubs raised errors if called; no health/mana reads occurred. git diff --check passed. The user subsequently confirmed player-frame hiding works in game.
- The user confirmed UnitHealthPercent and C_CurveUtil.CreateCurve exist on the beta client. Version 0.5.3 implements the researched curve-to-alpha path. Lua 5.1 simulations passed for comparison-rejecting secret-result sentinels, health boundaries (including 99.999% and 100%), maximum-health changes, target/combat transitions, deferred modes, Show hooks, missing-frame retry, saved-setting reapplication and existing targets; raw resource APIs were forbidden by the harness. git diff --check passed. The user subsequently confirmed the health/alpha behavior works in game.
- Do not report tests that were not run as passed.
- Version 0.16.2 passed Lua 5.1 simulations using the Forever container hierarchy without legacy named buttons or auraPools: on/off, saved-only startup, late container discovery and accurate pending feedback, ConfigureAuraContainer/UpdateAuras, Show/SetAlpha enforcement, combat-deferred on/off, child alpha inheritance, all commands and independence of target body, focus and player buffs. Existing status-bar regressions and git diff --check passed. Actual rendering remains unverified in game.
- Version 0.16.1 passed Lua 5.1 regression simulations where LH_HideMe handles the target event before Classic's UpdateAuras creates buff/debuff buttons, including creation during combat, deferred off, late TargetFrame loading, all on/off, alpha enforcement and focus-frame independence. Existing status-bar regressions and git diff --check passed. The simulated saved-mode scenario also enables hiding explicitly and does not independently verify saved-only startup. In-game confirmation remains pending.
- Version 0.16.0 passed Lua 5.1 simulations for legacy and pooled aura frames, on/off, Show/SetAlpha enforcement including combat, deferred off, invalid commands, target changes, new buttons, late loading, saved-setting reapplication, all on/off and focus-frame independence. Existing status-bar regressions and git diff --check passed. In-game verification remains pending.
- Version 0.15.0 passed Lua 5.1 simulations for health boundaries, target/combat transitions, combat-deferred removal, disabled bars remaining disabled, multiple exceptions, invalid syntax/ranges, all on/off preservation, saved-setting reapplication, late-loaded bars, Show hooks, secret-result direct forwarding and missing health API fallback. Existing 0.14.0 status-bar regression simulations and git diff --check passed. In-game verification remains pending.
- Version 0.14.0 passed Lua 5.1 syntax and simulations for permanent manager-wide hiding, legacy fallback frames, Show/SetAlpha enforcement including combat, deferred on/off, late-frame retry, saved-setting reapplication, invalid commands, bulk commands and individual overrides. Verified timer/deadline APIs and XP/level event registrations are absent. git diff --check passed. In-game verification remains pending.
- Version 0.13.0 passed Lua 5.1 syntax and simulations for all ten settings, on/off visibility, individual overrides, invalid/missing/extra arguments, combat-deferred changes, missing-frame retry, saved-setting reapplication, General-only tabs and permanent Combat Log hiding. git diff --check passed. In-game verification remains pending.
- Test all: on/off from mixed settings, individual overrides afterward, invalid/missing/extra arguments, status, combat deferral, missing-frame retry and /reload persistence. General-only tabs and permanent Combat Log hiding still apply with all off.
- Version 0.12.0 passed Lua 5.1 syntax and simulations for addons-icon on/off, Show and independent SetShown enforcement (used by Blizzard's addon-count updates), combat deferral, invalid commands, saved settings, late-frame retry and calendar-icon independence. git diff --check passed. In-game verification remains pending.
- Version 0.11.0 passed Lua 5.1 syntax and simulations for calendar-icon on/off, Show enforcement, combat-deferred modes, invalid commands, saved-setting reapplication, missing-frame retry and independence from Minimap, CalendarFrame and existing targets. git diff --check passed. In-game verification remains pending.
- Version 0.10.0 passed Lua 5.1 syntax and simulations for Show-before-focus activation, preserved active typing during mode changes, focus-loss hiding, off restoration after Hide without keyboard capture, new/temporary inputs, hook deduplication, chat updates, combat deferral, invalid commands, saved-setting reapplication, editBox fallback and chat-tab independence. git diff --check passed. In-game verification remains pending.
- Version 0.10.1 passed Lua 5.1 syntax and simulations for renamed commands, retained setting, chat input activation/focus loss, permanent Combat Log hiding, Show/SetAlpha enforcement, General selection fallback, late frame loading, reload reapplication and combat alpha enforcement. git diff --check passed. Native rendering still requires in-game verification.
- Version 0.9.1 passed Lua 5.1 syntax and simulations for General-only off/default behavior, all-hidden on, Show enforcement, temporary tabs, chat updates, combat-deferred on/off, saved-setting reapplication, ChatFrame1.tab fallback, preserved chat windows and independence from bag-bar. git diff --check passed. In-game verification remains pending.
- Version 0.9.0 passed Lua 5.1 syntax and chat-tab simulations for on/off, Show enforcement, hook deduplication, new/temporary windows, chat events, combat deferral, invalid commands, saved-setting reapplication, preserved text/edit frames and independence from chat-buttons. git diff --check passed. In-game verification remains pending.
- Version 0.8.0 passed Lua 5.1 syntax and chat-button simulations for resolved controls, on/off, Show enforcement, frame/function hook deduplication, new/temporary windows, chat update events, combat deferral, invalid commands, saved-setting reapplication, untargeted text/tab/edit frames and independence from other settings. git diff --check passed. The user subsequently confirmed chat-buttons works in game.
- Version 0.7.1 passed Lua 5.1 syntax and simulations for manager-wide alpha, Show/SetAlpha enforcement without recursion, XP pulse restart, level-up, expiry during combat, deferred off, timer cancellation, legacy XP/reputation fallback and independence from existing settings. Native rendering of borders and all child bar types still needs in-game verification.
- Version 0.7.0 passed Lua 5.1 syntax and XP-bar simulations for two-second expiry and restart, non-player filtering, level-up, off cancelling an active timer, combat expiry and deferred modes, Show hooks, legacy and managed XP frames, inactive/reputation bars remaining untouched, saved-setting reapplication, late loading and independence from other settings. git diff --check passed. In-game verification remains pending.
- Version 0.6.0 passed Lua 5.1 syntax and toolbar simulations for target/combat transitions, deferred on/off, inactive bars staying inactive, late-loaded bars, Show hooks, invalid commands, saved-setting reapplication and independence from the existing targets. The harness also verified toolbar state drivers were untouched. The user confirmed on October 11, 2026 that toolbars works in game; the full compatibility test matrix remains pending.
- The user confirmed version 0.9.1 General-only chat tabs work in game.
- Test chat-bar: Return opens input, typing and slash commands remain usable, Return sends and Escape cancels, on hides idle fields, off keeps General input visible without keyboard capture, other/new/temporary windows, combat deferral and /reload persistence.
- Test calendar-icon: on/off, invitation indicators, UI refreshes, combat-deferred changes, /reload persistence and independence from other minimap elements. Version 0.11.0 requires in-game verification.
- Test addons-icon: on/off, addon registration/UI refreshes, combat-deferred changes, /reload persistence and independence from calendar-icon. Version 0.12.0 requires in-game verification.
- Test in game: all ten targets independently with on/off, help, status, invalid commands, persistence across /reload and restarts, and changes during combat applied after combat ends.
- Test chat-tabs: on hides all tabs; off shows only General while Combat Log, Voice, unused and new/temporary tabs stay hidden. Also test docked/undocked windows, hover/chat updates, combat-deferred changes, persistence and independence from chat-buttons. Version 0.9.1 awaits in-game confirmation.
- Test chat-buttons: all available menu/channel/social/voice/scroll/minimize controls, multiple docked and undocked windows, new and temporary chat windows, combat-deferred changes, UI refreshes, off restoration, and continued text entry/tab selection/mouse-wheel scrolling. The user confirmed basic functionality in version 0.8.0; the full matrix remains pending.
- Test exp-bar: permanent border/content disappearance including reputation and other status bars through XP gains, level-ups and other status updates, combat, on/off during combat, /reload, late loading, maximum level, and independence from toolbar settings. Off restores available bars. Version 0.14.0 awaits in-game confirmation.
- Test toolbars: target select/clear, combat enter/leave, deferred mode changes, enabling/disabling additional bars while hiding is enabled, pet/stance/possess/override states, key bindings, and independence from bag-bar, micro-menu and player-frame settings.
- Also test the player frame: select/clear a target, enter/leave combat (including clearing a target during combat), enable with a target already selected, change modes during combat, lose health and regenerate to exactly full health. Mana changes must not affect visibility. Verify transparent-frame mouse behavior and off restoring alpha to 1.
- Verify that UI updates do not permanently reveal hidden elements and that off restores them.
- New addons require a game restart; changes to an already loaded LH_HideMe can be loaded with /reload.

## GitHub and execution environment

- Git and GitHub CLI are installed.
- The user configured authentication and Git identity in their Windows session.
- The previous agent environment ran as CodexSandboxOffline and could not use saved credentials or the global Git identity.
- An invalid-token message in that environment may be caused by separate user contexts; do not prematurely reset the user's authentication.
- Recheck permissions and authentication in future sessions.
- Do not store credentials in project files or outputs.
- Do not invent a commit identity.
- Commit and push according to the current user request. Previous publication does not authorize automatic future pushes.
- If access is unavailable, finish local work and provide concrete PowerShell commands for the user's normal session.
- Preserve unrelated changes; do not use destructive Git commands without authorization.

## Addon list artwork

- Version 0.13.1 adds a custom golden closed-eye icon with a violet glow in a hand-painted WoW style. No Lua behavior changes.
- Generated with the built-in image_gen tool, then converted to a 256x256 uncompressed BGRA TGA with top-left origin.
- IconTexture points to Interface\AddOns\LH_HideMe\Media\Icon (extension omitted). Keep Media when installing.
- Native addon-list rendering requires in-game verification. Restart WoW after adding the new texture if /reload does not show it.

- The addon now requires LH_Tweaks as its shared configuration host and load-order dependency. CurseForge releases must also declare the LH_Tweaks project as a required dependency.

## Native settings and shared icon (0.20.0)

- Settings.lua registers LH HideMe using LH_Tweaks:RegisterModule. Blizzard's native subcategory provides indentation and expansion under LH Tweaks. Thirteen hiding proxies and eight action bar exception proxies reuse the existing slash command implementation; the wrapper notifies the UI after every command, including early-return bulk and exception paths.
- Defaults are false for all 21 proxies, so native category reset disables hiding and clears exceptions. Hide all/Show all preserve exceptions. Settings remain per character in LH_HideMeDB; existing visibility and combat deferral are retained.
- TOC Title is LH HideMe; Group is LH_Tweaks (the exact parent folder identifier). The core TOC explicitly sets the same parent Group. This uses the native Forever AddonList grouping described in https://raw.githubusercontent.com/Gethe/wow-ui-source/forever/Interface/AddOns/Blizzard_AddOnList/AddonList.lua .
- Media/Icon.png and Media/Icon.tga are exact copies of the LH_Tweaks icon, using Spoken's chamfered gold frame reference and LH lettering. The README documents this. Historical closed-eye notes above describe the replaced artwork.
- .settings-test.py passes native module registration, all 21 settings, real visibility on/off, combat-deferred changes, slash/UI synchronization, scoped defaults, bulk exception preservation, saved values and byte-identical icons. Real in-game settings and grouping presentation remain pending. Restart WoW because the TOC gains Settings.lua and Group metadata.
