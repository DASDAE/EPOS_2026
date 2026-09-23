-- The readme needs absolute Pages URLs on GitHub; the rendered index needs
-- relative links so the same navigation works in local preview and on Pages.
function Link(link)
  local prefix = "https://dasdae.github.io/EPOS_2026/"
  if link.target:sub(1, #prefix) == prefix then
    local path = link.target:sub(#prefix + 1)
    link.target = path ~= "" and path or "./"
    return link
  end
end
