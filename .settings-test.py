import os
from pathlib import Path

addon = Path(__file__).resolve().parent
core = addon.parent / 'LH_Tweaks'
os.chdir(core)
exec((core / '.settings-test.py').read_text())
os.chdir(addon)
lua.execute('''
local M=getmetatable(UIParent).__index
function M:Show() self.shown=true end
function M:SetAlpha(v) self.alpha=v end
function UnitExists() return false end
BagsBar=CreateFrame('Frame',nil,UIParent)
MainActionBar=CreateFrame('Frame',nil,UIParent)
MainActionBar.EndCaps=CreateFrame('Frame',nil,MainActionBar)
MainActionBar.BorderArt=CreateFrame('Frame',nil,MainActionBar)
ActionButton1=CreateFrame('Button',nil,MainActionBar)
LH_HideMeDB={hideBagBar=true,toolbarExceptions={[2]=true}}
combat=false
''')
lua.execute((addon / 'LH_HideMe.lua').read_text(), 'LH_HideMe')
lua.execute("hideEvent=frames[#frames];hideEvent.scripts.OnEvent(hideEvent,'ADDON_LOADED','LH_HideMe')")
lua.execute((addon / 'Settings.lua').read_text(), 'LH_HideMe')
lua.execute('''
local module=LH_Tweaks.modules.LH_HideMe
local category=module.category
assert(module.title=='LH HideMe' and category.parent==LH_Tweaks.category)
local count=0
for variable,setting in pairs(registry) do
 if setting.category==category then
  assert(setting.default==false)
  setting.set(true);assert(setting.get(),variable)
  setting.set(false);assert(not setting.get(),variable)
  count=count+1
 end
end
assert(count==22,'Expected 14 hiding options and 8 health exceptions')
-- Forever bar artwork is independent of the action buttons and other bars.
registry.LH_HideMe_bar_artwork.set(true)
for _,region in ipairs({MainActionBar.EndCaps,MainActionBar.BorderArt}) do assert(region.alpha==0) end
assert(ActionButton1.alpha==nil and MainActionBar.alpha==1)
MainActionBar.EndCaps:SetAlpha(1)
assert(MainActionBar.EndCaps.alpha==0)
registry.LH_HideMe_bar_artwork.set(false)
for _,region in ipairs({MainActionBar.EndCaps,MainActionBar.BorderArt}) do assert(region.alpha==1) end
combat=true;registry.LH_HideMe_bar_artwork.set(true)
assert(MainActionBar.EndCaps.alpha==1 and LH_HideMeDB.hideBarArtwork)
combat=false;hideEvent.scripts.OnEvent(hideEvent,'PLAYER_REGEN_ENABLED')
assert(MainActionBar.EndCaps.alpha==0)
registry.LH_HideMe_bar_artwork.set(false)
-- UI calls the existing secure/deferred visibility implementation.
registry.LH_HideMe_bag_bar.set(true);assert(not BagsBar.shown)
registry.LH_HideMe_bag_bar.set(false);assert(BagsBar.shown)
combat=true;registry.LH_HideMe_bag_bar.set(true)
assert(BagsBar.shown and LH_HideMeDB.hideBagBar)
combat=false;hideEvent.scripts.OnEvent(hideEvent,'PLAYER_REGEN_ENABLED')
assert(not BagsBar.shown)
-- Slash changes notify the same settings and bulk toggles retain exceptions.
SlashCmdList.LH_HIDEME('except toolbar 3')
assert(registry.LH_HideMe_toolbarException3.get() and notices.LH_HideMe_toolbarException3>0)
buttons['Enable every hiding option']()
for name in pairs(LH_HideMe.targets) do assert(LH_HideMe:GetOption(name)) end
buttons['Disable every hiding option']()
for name in pairs(LH_HideMe.targets) do assert(not LH_HideMe:GetOption(name)) end
assert(LH_HideMe:GetToolbarException(3))
-- Native Defaults applies the default value to this category's proxies only.
LH_TweaksDB.autoRepair=true
for _,setting in pairs(registry) do if setting.category==category then setting.set(setting.default) end end
assert(not LH_HideMe:GetToolbarException(3) and LH_TweaksDB.autoRepair)
-- Saved character state is reloaded by the existing initialization path.
LH_HideMeDB.hideBagBar=true;LH_HideMeDB.toolbarExceptions[8]=true
hideEvent.scripts.OnEvent(hideEvent,'ADDON_LOADED','LH_HideMe')
assert(registry.LH_HideMe_bag_bar.get() and registry.LH_HideMe_toolbarException8.get())
SettingsPanel:DisplayCategory(category)
assert(SettingsPanel.list.Header.Title.text=='LH HideMe')
''')
assert (addon / 'Media/Icon.tga').read_bytes() == (core / 'Icon.tga').read_bytes()
assert (addon / 'Media/Icon.png').read_bytes() == (core / 'Icon.png').read_bytes()
print('PASS: nested module category, all 22 controls, artwork isolation and combat deferral, command/UI synchronization, scoped defaults, bulk preservation, saved settings and identical icons')
