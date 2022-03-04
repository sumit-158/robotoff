import itertools

from lark import Lark, Transformer
from lark.visitors import Discard


class PackagingTransformer(Transformer):
    def to_recycling(self, items):
        return {"recycling": items[1].value}

    def shape_material(self, items):
        shape_items = [x for x in items if x.type == "SHAPES"]
        assert len(shape_items) == 1
        material_items = [x for x in items if x.type == "MATERIALS"]
        assert len(material_items) == 1
        return {"shape": shape_items[0].value, "material": material_items[0].value}

    def packaging(self, items):
        assert len(items) in (1, 2)
        if isinstance(items[0], dict):
            output = items[0]
        else:
            output = {"shape": items[0].value}
        if len(items) == 2:
            output.update(items[1])
        return [output]

    def multiple_packaging(self, items):
        output = []
        assert len(items) in (2, 3)
        shape_item = items[0]
        assert shape_item.type == "SHAPES"
        shape_materials_item = items[1]
        base_dict = {"material": shape_materials_item["material"]}

        if len(items) == 3:
            base_dict.update(items[2])

        output.append({"shape": shape_item.value, **base_dict})
        output.append({**shape_materials_item, **base_dict})
        return output

    def junk(self, items):
        return Discard

    def start(self, items):
        return list(itertools.chain.from_iterable(items))


parser = Lark(open("grammars/packaging.lark", "r").read(), parser="lalr")

tree = parser.parse(
    """Liste des emballages: opercule en plastique à recycler, canette en aluminium recyclé, à mettre dans le conteneur à pa
 pier. Opercule et film en plastique. boite et couvercle metal à recycler. Boîte à recycler dans le conteneur à papier ! Pensez au tri !""",
)

print(tree.pretty())
print(PackagingTransformer().transform(tree))

# [
#     {"shape": "opercule", "material": "plastique", "recycling": "recycler"},
#     {"shape": "canette", "material": "aluminium"},
#     {"shape": "Opercule", "material": "plastique"},
#     {"shape": "film", "material": "plastique"},
#     {"shape": "boite", "material": "metal", "recycling": "recycler"},
#     {"shape": "couvercle", "material": "metal", "recycling": "recycler"},
#     {"shape": "Couvercle"},
# ]
