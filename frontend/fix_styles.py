with open("/Users/henry/Aegis360/frontend/src/views/dpo/DpoQuestionManagementView.vue", "r") as f:
    content = f.read()

# Replace the nested "<style scoped>" with just a newline or empty string
# The first "<style scoped>" is at the top of the CSS block.
# We just need to find the SECOND "<style scoped>" and remove it, and make sure there is a closing "</style>" at the end of the file.

content = content.replace("\n<style scoped>\n.dashboard-layout", "\n.dashboard-layout")

if not content.strip().endswith("</style>"):
    content += "\n</style>\n"

with open("/Users/henry/Aegis360/frontend/src/views/dpo/DpoQuestionManagementView.vue", "w") as f:
    f.write(content)

print("Fixed styles!")
