local addonName = ...
local Addon = LH_HideMe
local variables = {}
local notifying = false

local function Refresh()
    if notifying or not Settings or not Settings.NotifyUpdate then return end
    notifying = true
    for _, variable in ipairs(variables) do Settings.NotifyUpdate(variable) end
    notifying = false
end

local originalCommand = SlashCmdList.LH_HIDEME
SlashCmdList.LH_HIDEME = function(message)
    originalCommand(message)
    Refresh()
end

local function Command(message) SlashCmdList.LH_HIDEME(message) end
local function Header(layout, title)
    layout:AddInitializer(CreateSettingsListSectionHeaderInitializer(title))
end

local sections = {
    { title = "Chat", options = {
        { "chat-bar", "Hide idle chat input", "Hide the input field while idle. Press Enter to type. Disabled keeps the General input visible without taking focus." },
        { "chat-buttons", "Hide chat buttons and scroll controls", "Hide buttons and scroll controls on standard chat windows." },
        { "chat-tabs", "Hide all chat tabs", "Hide all standard chat tabs. When disabled, only the General tab is shown. The Combat Log stays hidden in both modes." },
    } },
    { title = "Minimap", options = {
        { "addons-icon", "Hide the addon menu icon", "Hide the minimap addon compartment button." },
        { "calendar-icon", "Hide the calendar icon", "Hide the minimap calendar button and its invitation indicators." },
        { "day-night-indicator", "Hide the day/night indicator", "Hide the minimap day/night indicator and its border." },
    } },
    { title = "Interface", options = {
        { "bag-bar", "Hide the bag bar", "Hide the standard bag bar." },
        { "micro-menu", "Hide the micro menu", "Hide the standard micro menu." },
        { "exp-bar", "Hide status bars", "Permanently hide experience, reputation and other status bars, including their borders." },
        { "fishing-bobber-tooltip", "Hide the fishing bobber tooltip", "Suppress the world tooltip for fishing bobbers on English and German clients." },
        { "targetauras", "Hide target buffs and debuffs", "Hide aura artwork on Blizzard's target frame." },
    } },
    { title = "Conditional visibility", options = {
        { "player-frame", "Hide the player frame when idle at full health", "Show the player frame with a target, in combat or below full health. Without the required health API, target and combat visibility are used." },
        { "toolbars", "Hide action bars when idle", "Show active standard action bars with a target or in combat, including available pet, stance and shaman totem bars. Key bindings remain usable." },
    } },
}

local function Build(category, layout)
    Addon.category = category
    for _, section in ipairs(sections) do
        Header(layout, section.title)
        for _, option in ipairs(section.options) do
            local name, label, tooltip = option[1], option[2], option[3]
            local variable = "LH_HideMe_" .. name:gsub("-", "_")
            variables[#variables + 1] = variable
            local setting = Settings.RegisterProxySetting(category, variable, "boolean", label, false,
                function() return Addon:GetOption(name) end,
                function(value) Command(name .. (value and " on" or " off")) end)
            Settings.CreateCheckbox(category, setting, tooltip .. " Saved per character. Changes made during combat take effect afterward.")
        end
    end
    Header(layout, "Action bar health exceptions")
    for number = 1, 8 do
        local variable = "LH_HideMe_toolbarException" .. number
        variables[#variables + 1] = variable
        local setting = Settings.RegisterProxySetting(category, variable, "boolean",
            "Show action bar " .. number .. " below full health", false,
            function() return Addon:GetToolbarException(number) end,
            function(value) Command("except toolbar " .. number .. (value and "" or " off")) end)
        Settings.CreateCheckbox(category, setting,
            "While action-bar hiding is enabled, also show this active bar below full health. Numbers match the game's action bar settings. Requires the health API. Saved exceptions are retained by Hide all and Show all.")
    end
    Header(layout, "All hiding options")
    layout:AddInitializer(CreateSettingsButtonInitializer("Enable every hiding option", "Hide all",
        function() Command("all on") end, "Enable all 13 hiding options. Keep action bar health exceptions.", true))
    layout:AddInitializer(CreateSettingsButtonInitializer("Disable every hiding option", "Show all",
        function() Command("all off") end, "Disable hiding options. Only the General chat tab is shown; the Combat Log remains hidden. Keep action bar health exceptions.", true))
end

-- The required core queues this page until its root category is ready.
LH_Tweaks:RegisterModule(addonName, "LH HideMe", Build)
