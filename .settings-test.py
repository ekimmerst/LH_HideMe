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
function GameTooltip:HookScript() end
function GameTooltip:IsShown() return false end
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
lua.execute('''
function Settings.CreateElementInitializer(template, data)
 local row={template=template,data=data,tags={}}
 function row:AddSearchTags(tag) self.tags[#self.tags+1]=tag end
 function row:GetData() return self.data end
 return row
end
''')
lua.execute((addon / 'Settings.lua').read_text(), 'LH_HideMe')
lua.execute('''
local module=LH_Tweaks.modules.LH_HideMe
local category=module.category
assert(module.title=='LH HideMe' and category.parent==LH_Tweaks.category)
assert(#category.layout.rows==3)
local rows=category.layout.rows
assert(rows[1].template=='LHHideMeSettingsRowTemplate')
assert(rows[1].data.sections[1].title=='Chat' and rows[1].data.sections[2].title=='Minimap')
assert(rows[2].data.sections[1].title=='Interface' and rows[2].data.sections[2].title=='Conditional visibility')
assert(rows[3].data.sections[1].title=='Action bar health exceptions')
assert(#rows[1].data.sections[1].options==3 and #rows[1].data.sections[2].options==3)
assert(#rows[2].data.sections[1].options==6 and #rows[2].data.sections[2].options==2)
assert(#rows[3].data.sections[1].options==4 and #rows[3].data.sections[2].options==4)
for _,row in ipairs(rows) do assert(row:GetExtent()==row.data.height and #row.tags>0) end
local M=getmetatable(UIParent).__index
function M:SetHeight(height) self.h=height end
function M:SetWidth(width) self.w=width end
function M:SetJustifyH() end
function M:SetChecked(value) self.checked=value end
function M:GetChecked() return self.checked end
function M:CreateFontString() return CreateFrame('FontString',nil,self) end
local row=CreateFrame('Frame',nil,UIParent)
for name,method in pairs(LHHideMeSettingsRowMixin) do row[name]=method end
row:Init(rows[1])
assert(row.headers[1].text=='Chat' and row.headers[2].text=='Minimap')
assert(row.checkboxes[1].optionName=='chat-bar' and row.checkboxes[4].optionName=='addons-icon')
row.checkboxes[1]:SetChecked(true);row.checkboxes[1].scripts.OnClick(row.checkboxes[1])
assert(LH_HideMe:GetOption('chat-bar') and row.checkboxes[1]:GetChecked())
row:Init(rows[3])
assert(row.checkboxes[1].optionName=='except toolbar 1' and row.checkboxes[5].optionName=='except toolbar 5')
row.checkboxes[1]:SetChecked(true);row.checkboxes[1].scripts.OnClick(row.checkboxes[1])
assert(LH_HideMe:GetToolbarException(1) and row.checkboxes[1]:GetChecked())
row:Release()
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
SettingsPanel:DisplayCategory(category)
local header=SettingsPanel.list.Header
local hideAll,showAll=header.children[2],header.children[3]
assert(hideAll.text=='Hide all' and showAll.text=='Show all')
assert(showAll.points[1][2]==header.DefaultsButton and hideAll.points[1][2]==showAll)
hideAll:Click()
for name in pairs(LH_HideMe.targets) do assert(LH_HideMe:GetOption(name)) end
showAll:Click()
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
SettingsPanel:DisplayCategory(LH_Tweaks.category)
assert(hideAll.text=='Enable all' and showAll.text=='Disable all')
SettingsPanel:DisplayCategory(category)
assert(hideAll.text=='Hide all' and showAll.text=='Show all')
''')
assert (addon / 'Media/Icon.tga').read_bytes() == (core / 'Icon.tga').read_bytes()
assert (addon / 'Media/Icon.png').read_bytes() == (core / 'Icon.png').read_bytes()
print('PASS: two-column settings rows and clicks, all 22 proxies, artwork isolation and combat deferral, command/UI synchronization, scoped defaults, bulk preservation, saved settings and identical icons')
