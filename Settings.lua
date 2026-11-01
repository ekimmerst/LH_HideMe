local addonName = ...
local Addon = LH_HideMe
local variables = {}
local notifying = false
local visibleRows = setmetatable({}, { __mode = "k" })

local function Refresh()
    if notifying then return end
    notifying = true
    if Settings and Settings.NotifyUpdate then
        for _, variable in ipairs(variables) do Settings.NotifyUpdate(variable) end
    end
    for row in pairs(visibleRows) do row:Refresh() end
    notifying = false
end

local originalCommand = SlashCmdList.LH_HIDEME
SlashCmdList.LH_HIDEME = function(message)
    originalCommand(message)
    Refresh()
end

local function Command(message) SlashCmdList.LH_HIDEME(message) end
local sections = {
    { title = "Chat", options = {
        { "chat-bar", "Hide idle chat input", "Hide the input field while idle. Press Enter to type. Disabled keeps the General input visible without taking focus." },
        { "chat-buttons", "Hide chat buttons and scroll controls", "Hide buttons and scroll controls on standard chat windows." },
        { "chat-tabs", "Hide General and Combat Log tabs", "Hide the General tab. The Combat Log stays hidden in both modes; other tabs, including whispers, follow the game's visibility." },
    } },
    { title = "Minimap", options = {
        { "addons-icon", "Hide the addon menu icon", "Hide the minimap addon compartment button." },
        { "calendar-icon", "Hide the calendar icon", "Hide the minimap calendar button and its invitation indicators." },
        { "day-night-indicator", "Hide the day/night indicator", "Hide the minimap day/night indicator and its border." },
    } },
    { title = "Interface", options = {
        { "bar-artwork", "Hide action bar artwork", "Hide the main bar border and gryphons independently of action buttons, bags and the micro menu." },
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

local exceptionSection = { title = "Action bar health exceptions", options = {} }
for number = 1, 8 do
    exceptionSection.options[number] = {
        "except toolbar " .. number,
        "Show action bar " .. number .. " below full health",
        "While action-bar hiding is enabled, also show this active bar below full health. Numbers match the game's action bar settings. Requires the health API. Saved exceptions are retained by Hide all and Show all.",
    }
end

local function GetOptionValue(name)
    local number = name:match("^except toolbar (%d+)$")
    if number then return Addon:GetToolbarException(tonumber(number)) end
    return Addon:GetOption(name)
end

LHHideMeSettingsRowMixin = {}

function LHHideMeSettingsRowMixin:Refresh()
    for _, checkbox in ipairs(self.checkboxes or {}) do
        if checkbox:IsShown() then checkbox:SetChecked(GetOptionValue(checkbox.optionName)) end
    end
end

function LHHideMeSettingsRowMixin:Init(initializer)
    local data = initializer:GetData()
    self:SetHeight(data.height)
    self.headers = self.headers or {}
    self.checkboxes = self.checkboxes or {}
    for _, header in ipairs(self.headers) do header:Hide() end
    for _, checkbox in ipairs(self.checkboxes) do checkbox:Hide() end

    local checkboxIndex = 0
    for column, section in ipairs(data.sections) do
        local x = column == 1 and 8 or 318
        local header = self.headers[column]
        if not header then
            header = self:CreateFontString(nil, "ARTWORK", "GameFontNormalLarge")
            self.headers[column] = header
        end
        header:ClearAllPoints()
        header:SetPoint("TOPLEFT", self, "TOPLEFT", x, -8)
        header:SetText(section.title)
        header:Show()

        for index, option in ipairs(section.options) do
            checkboxIndex = checkboxIndex + 1
            local checkbox = self.checkboxes[checkboxIndex]
            if not checkbox then
                checkbox = CreateFrame("CheckButton", nil, self, "UICheckButtonTemplate")
                checkbox:SetSize(26, 26)
                checkbox.label = checkbox:CreateFontString(nil, "ARTWORK", "GameFontHighlight")
                checkbox.label:SetJustifyH("LEFT")
                checkbox.label:SetWidth(268)
                checkbox.label:SetPoint("LEFT", checkbox, "RIGHT", 2, 0)
                self.checkboxes[checkboxIndex] = checkbox
            end
            checkbox:ClearAllPoints()
            checkbox:SetPoint("TOPLEFT", self, "TOPLEFT", x, -32 - (index - 1) * 38)
            checkbox.optionName = option[1]
            checkbox.tooltipText = option[3] .. " Saved per character. Changes made during combat take effect afterward."
            checkbox.label:SetText(option[2])
            checkbox:SetScript("OnClick", function(self)
                local name = self.optionName
                local mode = self:GetChecked() and (name:match("^except toolbar") and "" or " on") or " off"
                Command(name .. mode)
            end)
            checkbox:SetScript("OnEnter", function(self)
                GameTooltip:SetOwner(self, "ANCHOR_RIGHT")
                GameTooltip:SetText(self.label:GetText(), 1, 1, 1)
                GameTooltip:AddLine(self.tooltipText, nil, nil, nil, true)
                GameTooltip:Show()
            end)
            checkbox:SetScript("OnLeave", function() GameTooltip:Hide() end)
            checkbox:Show()
        end
    end
    self:Refresh()
    visibleRows[self] = true
end

function LHHideMeSettingsRowMixin:Release()
    visibleRows[self] = nil
end

local function AddRow(layout, left, right, splitOptions)
    local rowSections = {}
    if splitOptions then
        rowSections[1] = { title = left.title, options = {} }
        rowSections[2] = { title = "", options = {} }
        for number, option in ipairs(left.options) do
            rowSections[number <= 4 and 1 or 2].options[#rowSections[number <= 4 and 1 or 2].options + 1] = option
        end
    else
        rowSections = { left, right }
    end
    local maxOptions = math.max(#rowSections[1].options, #rowSections[2].options)
    local initializer = Settings.CreateElementInitializer("LHHideMeSettingsRowTemplate", {
        sections = rowSections,
        height = 32 + maxOptions * 38,
    })
    initializer.GetExtent = function() return 32 + maxOptions * 38 end
    for _, section in ipairs(rowSections) do
        initializer:AddSearchTags(section.title)
        for _, option in ipairs(section.options) do initializer:AddSearchTags(option[2]) end
    end
    layout:AddInitializer(initializer)
end

local function Build(category, layout)
    Addon.category = category
    LH_Tweaks:RegisterHeaderActions(category,
        {text = "Hide all", callback = function() Command("all on") end,
            tooltip = "Enable all 14 hiding options. Keep action bar health exceptions."},
        {text = "Show all", callback = function() Command("all off") end,
            tooltip = "Disable hiding options. The General tab is shown, the Combat Log remains hidden, and other chat tabs follow the game. Keep action bar health exceptions."})
    for _, section in ipairs(sections) do
        for _, option in ipairs(section.options) do
            local name, label = option[1], option[2]
            local variable = "LH_HideMe_" .. name:gsub("-", "_")
            variables[#variables + 1] = variable
            Settings.RegisterProxySetting(category, variable, "boolean", label, false,
                function() return Addon:GetOption(name) end,
                function(value) Command(name .. (value and " on" or " off")) end)
        end
    end
    for number = 1, 8 do
        local variable = "LH_HideMe_toolbarException" .. number
        variables[#variables + 1] = variable
        Settings.RegisterProxySetting(category, variable, "boolean",
            "Show action bar " .. number .. " below full health", false,
            function() return Addon:GetToolbarException(number) end,
            function(value) Command("except toolbar " .. number .. (value and "" or " off")) end)
    end
    AddRow(layout, sections[1], sections[2])
    AddRow(layout, sections[3], sections[4])
    AddRow(layout, exceptionSection, nil, true)
end

-- The required core queues this page until its root category is ready.
LH_Tweaks:RegisterModule(addonName, "LH HideMe", Build)
