from treeland_windowtree import WindowTreeClient

client = WindowTreeClient()
layers = client.get_full_layout_tree()
cursor = client.cursor_position()

print(f"{layers}")
