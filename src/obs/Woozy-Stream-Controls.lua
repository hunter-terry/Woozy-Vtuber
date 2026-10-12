obs = obslua
local last_width, last_height = -1, -1

function script_description()
    return 'Keeps Woozy in the approved bottom-right stream position when the Lens Studio streaming preview window changes size. Uses the saved Woozy Streaming workspace and C920 16:9 preview. Does not change the character, tracking, audio, or blue key.'
end

local function frame_preview()
    local scene_source = obs.obs_get_source_by_name('Scene')
    if scene_source == nil then return end
    local ok, err = pcall(function()
    local scene = obs.obs_scene_from_source(scene_source)
    local item = scene and obs.obs_scene_find_source(scene, 'Woozy Preview')
    if item ~= nil then
        local source = obs.obs_sceneitem_get_source(item)
        local width = obs.obs_source_get_width(source)
        local height = obs.obs_source_get_height(source)
        if width >= 500 and height >= 350 and (width ~= last_width or height ~= last_height) then
            -- Streaming workspace: toolbar above, status bar below, centered 16:9 live viewport.
            local available_width = width - 10
            local available_height = height - 124 - 28
            local viewport_width = math.min(available_width, available_height * 16 / 9)
            local viewport_height = viewport_width * 9 / 16
            local viewport_left = (width - viewport_width) / 2
            local viewport_top = 124 + (available_height - viewport_height) / 2
            local crop = obs.obs_sceneitem_crop()
            crop.left = math.floor(viewport_left + viewport_width * 0.1923 + 0.5)
            crop.right = math.floor(width - viewport_left - viewport_width * 0.8077 + 0.5)
            crop.top = math.floor(viewport_top + 10 + 0.5)
            crop.bottom = math.floor(height - viewport_top - viewport_height * 0.92 + 0.5)
            obs.obs_sceneitem_set_crop(item, crop)
            -- OBS alignment bit flags are C macros, not exported Lua constants: left=1, top=4, bottom=8.
            obs.obs_sceneitem_set_alignment(item, 5)
            obs.obs_sceneitem_set_bounds_type(item, obs.OBS_BOUNDS_SCALE_INNER)
            obs.obs_sceneitem_set_bounds_alignment(item, 9)
            local bounds = obs.vec2()
            bounds.x, bounds.y = 312, 262
            obs.obs_sceneitem_set_bounds(item, bounds)
            local position = obs.vec2()
            position.x, position.y = 1608, 819
            obs.obs_sceneitem_set_pos(item, position)
            obs.obs_sceneitem_set_locked(item, true)
            last_width, last_height = width, height
            obs.script_log(obs.LOG_INFO, string.format('Woozy auto-frame: capture %dx%d, crop L%d T%d R%d B%d', width, height, crop.left, crop.top, crop.right, crop.bottom))
        end
    end
    end)
    obs.obs_source_release(scene_source)
    if not ok then
        obs.timer_remove(frame_preview)
        obs.script_log(obs.LOG_WARNING, 'Woozy framing stopped safely: ' .. tostring(err))
    end
end

local function open_woozy_if_needed()
    local project = (script_path() .. 'Woozy-Headroom-Review/Lens-Project/Woozy-Goo-Face-Live-Test.esproj'):gsub('/', '\\')
    local lens = 'C:\\Users\\hunte\\AppData\\Local\\Programs\\Lens Studio\\Lens Studio.exe'
    local command = 'tasklist /FI "IMAGENAME eq Lens Studio.exe" /NH | find /I "Lens Studio.exe" >nul || start "" "' .. lens .. '" "' .. project .. '"'
    local ok, result = pcall(os.execute, command)
    if not ok then
        obs.script_log(obs.LOG_WARNING, 'Woozy project could not be opened: ' .. tostring(result))
    end
end

function script_load(settings)
    open_woozy_if_needed()
    obs.timer_add(frame_preview, 250)
    frame_preview()
end

function script_unload()
    obs.timer_remove(frame_preview)
end
