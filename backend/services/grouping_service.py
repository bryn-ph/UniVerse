# services/grouping_service.py
from models import db, Class
from models import Tag  # your Tag model
from models import ClassGroup, ClassGroupMap
from utils.grouping import make_signature, normalize_tokens, jaccard

def assign_class_to_group(class_obj: Class, threshold: float = 0.4):
    """Attach class to an existing group by signature/similarity or create a new one."""
    tag_names = [t.name for t in (class_obj.tags or [])]
    sig = make_signature(class_obj.name, tag_names)

    # 1) exact signature
    group = ClassGroup.query.filter_by(signature=sig).first()
    if group:
        _link(class_obj, group)
        return group

    # 2) fuzzy (token Jaccard) across existing groups
    new_tokens = set(normalize_tokens(class_obj.name, tag_names))
    best, best_score = None, 0.0
    for g in ClassGroup.query.all():
        g_tokens = set(g.signature.split("-"))
        score = jaccard(new_tokens, g_tokens)
        if score > best_score:
            best, best_score = g, score

    if best and best_score >= threshold:
        _link(class_obj, best)
        return best

    # 3) no match -> create
    label = _label_from_tokens(list(new_tokens))
    group = ClassGroup(name=label, signature=sig, label=label)
    db.session.add(group)
    db.session.flush()  # get group.id
    _link(class_obj, group)
    db.session.commit()
    return group

def _link(class_obj: Class, group: ClassGroup):
    # Set the direct foreign key
    class_obj.class_group_id = group.id
    
    # Also create/update the mapping table entry
    mapping = ClassGroupMap.query.filter_by(class_id=class_obj.id).first()
    if mapping:
        mapping.group_id = group.id
    else:
        db.session.add(ClassGroupMap(class_id=class_obj.id, group_id=group.id))
    db.session.flush()

def _label_from_tokens(tokens: list[str]) -> str:
    words = [t for t in tokens if not t.isdigit()]
    return " ".join(w.capitalize() for w in words[:3]) or "General"
