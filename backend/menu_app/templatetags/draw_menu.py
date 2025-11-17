from django import template
from django.urls import resolve, Resolver404

from ..models import Menu

register = template.Library()


def build_tree(items, parent=None):
    """Строит дерево из списка элементов."""
    tree = []
    for item in items:
        if item.parent_id == (parent.id if parent else None):
            item.children = build_tree(items, item)
            tree.append(item)
    return tree


def mark_active_path(tree, active_item):
    """Помечает активный путь и раскрывает нужные уровни."""
    def walk(node):
        is_on_path = (node == active_item)
        for child in node.children:
            if walk(child):
                is_on_path = True
        node.is_active = (node == active_item)
        node.is_expanded = is_on_path or (
            node.is_active and node.parent is None)
        # Раскрываем первый уровень под активным
        if node.is_active:
            for child in node.children:
                child.is_expanded = True
        return is_on_path

    for root in tree:
        walk(root)


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_items': [], 'menu_name': menu_name}
    items = list(menu.items.select_related('parent').all())
    # Определяем активный пункт по URL
    current_url = request.path_info
    active_item = None
    for item in items:
        item_url = item.get_absolute_url()
        if item_url == current_url:
            active_item = item
            break
        try:
            match = resolve(current_url)
            if item.named_url and match.url_name == item.named_url:
                active_item = item
                break
        except Resolver404:
            pass
    # Строим дерево
    tree = build_tree(items)
    # Помечаем активный путь и раскрываем
    if active_item:
        mark_active_path(tree, active_item)
    else:
        # Если ничего не активно — раскрываем только корень
        for root in tree:
            root.is_expanded = True
    return {
        'menu_items': tree,
        'menu_name': menu_name,
        'request': request,
    }
