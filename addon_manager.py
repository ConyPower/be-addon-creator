import pathlib, json, uuid, shutil, enum, json_fix
from util import error, OUT_DIRECTORY

DEBUG = True


def debug(message: str):
    """
    DEBUG
    """
    if DEBUG:
        print(f"DEBUG: {message}")


# TODO: maybe make these editable?
FORMAT_VERSION = 2
FORMAT_VERSION_ITEM = "1.16.100"
FORMAT_VERSION_BLOCK = "1.19.80"
FORMAT_VERSION_BLOCK_SOUND = [1, 1, 0]
FORMAT_VERSION_RECIPE = "1.17.41"
MIN_ENGINE_VERSION = [1, 19, 0]
GLOBAL_VERSION = [1, 0, 0]


class BlockSounds(enum.Enum):
    AMETHYST_BLOCK = "amethyst_block"
    AMETHYST_CLUSTER = "amethyst_cluster"
    ANCIENT_DEBRIS = "ancient_debris"
    ANVIL = "anvil"
    AZALEA = "azalea"
    AZALEA_LEAVES = "azalea_leaves"
    BAMBOO = "bamboo"
    BAMBOO_SAPLING = "bamboo_sapling"
    BASALT = "basalt"
    BIG_DRIPLEAF = "big_dripleaf"
    BONE_BLOCK = "bone_block"
    CALCITE = "calcite"
    CANDLE = "candle"
    CAVE_VINES = "cave_vines"
    CHAIN = "chain"
    CLOTH = "cloth"
    COMPARATOR = "comparator"
    COPPER = "copper"
    CORAL = "coral"
    DEEPSLATE = "deepslate"
    DEEPSLATE_BRICKS = "deepslate_bricks"
    DIRT_WITH_ROOTS = "dirt_with_roots"
    DRIPSTONE_BLOCK = "dripstone_block"
    FROG_SPAWN = "frog_spawn"
    FROG_LIGHT = "froglight"
    FUNGUS = "fungus"
    GLASS = "glass"
    GRASS = "grass"
    GRAVEL = "gravel"
    HANGING_ROOTS = "hanging_roots"
    HONEY_BLOCK = "honey_block"
    ITEM_FRAME = "itemframe"
    LADDER = "ladder"
    LANTERN = "lantern"
    LARGE_AMETHYST_BUD = "large_amethyst_bud"
    SMALL_AMETHYST_BUD = "small_amethyst_bud"
    LEVER = "lever"
    LODESTONE = "lodestone"
    MANGROVE_ROOTS = "mangrove_roots"
    MUDDY_MANGROVE_ROOTS = "muddy_mangrove_roots"
    MEDIUM_AMETHYST_BUD = "medium_amethyst_bud"
    METAL = "metal"
    MOSS_BLOCK = "moss_block"
    MOSS_CARPET = "moss_carpet"
    MUD = "mud"
    MUD_BRICKS = "mud_bricks"
    NETHER_BRICK = "nether_brick"
    NETHER_GOLD_ORE = "nether_gold_ore"
    NETHER_SPROUTS = "nether_sprouts"
    NETHER_WART = "nether_wart"
    NETHER_WOOD = "nether_wood"
    NETHERITE = "netherite"
    NETHERRACK = "netherrack"
    NYLIUM = "nylium"
    PACKED_MUD = "packed_mud"
    POINTED_DRIPSTONE = "pointed_dripstone"
    POWDER_SNOW = "powder_snow"
    ROOTS = "roots"
    SAND = "sand"
    SCAFFOLDING = "scaffolding"
    SCULK = "sculk"
    SCULK_CATALYST = "sculk_catalyst"
    SCULK_SENSOR = "sculk_sensor"
    SCULK_SHRIEKER = "sculk_shrieker"
    SCULK_VEIN = "sculk_vein"
    SHROOM_LIGHT = "shroomlight"
    SLIME = "slime"
    SNOW = "snow"
    SOUL_SAND = "soul_sand"
    SOUL_SOIL = "soul_soil"
    SPORE_BLOSSOM = "spore_blossom"
    STEM = "stem"
    STONE = "stone"
    SWEET_BERRY_BUSH = "sweet_berry_bush"
    TUFF = "tuff"
    VINES = "vines"
    WOOD = "wood"


class CreativeCategory(enum.Enum):
    """
    A enum consisting of the Bedrock Edition creative tabs
    """

    CONSTRUCTION = "Construction"
    EQUIPMENT = "Equipment"
    ITEMS = "Items"
    NATURE = "Nature"


class RecipeShaped:
    """
    A minecraft bedrock shaped recipe
    """

    item_id: str
    pattern: list[str]

    def __init__(self) -> None:
        self.pattern = []
        self.item_id = ""

    def set_pattern(self, pattern: list[str]):
        self.pattern = pattern
        return self

    def set_item_id(self, item_id: str):
        self.item_id = item_id
        return self

    def construct(self, namespace: str) -> dict:
        """
        Returns the shaped recipe json used inside a behaviour pack
        """
        return {
            "format_version": FORMAT_VERSION_RECIPE,
            "minecraft:recipe_shaped": {
                "description": {"identifier": f"{namespace}:{self.item_id}"},
                "tags": ["crafting_table"],
                "pattern": self.pattern,
                "key": {
                    # TODO: work this out
                },
                "result": f"{namespace}:{self.item_id}",
            },
        }


class RecipeIngredient:
    """
    A minecraft bedrock shapeless recipe ingredient
    """

    item_id: str
    count: int

    def __init__(self, item_id: str, count: int) -> None:
        self.item_id = item_id
        self.count = count

    def __json__(self):
        return self.__dict__


class RecipeShapeless:
    """
    A minecraft bedrock shapeless recipe
    """

    item_id: str
    ingredients: list[RecipeIngredient]

    def __init__(self) -> None:
        self.ingredients = []
        self.item_id = ""

    def set_ingredients(self, ingredients: list[RecipeIngredient]):
        self.ingredients = ingredients
        return self

    def set_item_id(self, item_id: str):
        self.item_id = item_id
        return self

    def construct(self, namespace: str) -> dict:
        """
        Returns the shaped recipe json used inside a behaviour pack
        """
        return {
            "format_version": FORMAT_VERSION_RECIPE,
            "minecraft:recipe_shapeless": {
                "description": {"identifier": f"{namespace}:{self.item_id}"},
                "tags": ["crafting_table"],
                "ingredients": self.ingredients,
                "result": f"{namespace}:{self.item_id}",
            },
        }


class Item:
    """
    A minecraft bedrock item
    """

    id: str
    display_name: str
    texture_path: str | None
    category: CreativeCategory
    max_stack_size: int

    is_food: bool
    food_bars: int

    recipe: RecipeShaped | RecipeShapeless | None

    def __init__(self) -> None:
        self.id = "placeholder"
        self.display_name = "Placeholder"
        self.texture_path = (
            None  # If None, it will use the default path that uses id as file name
        )
        self.category = CreativeCategory.CONSTRUCTION
        self.max_stack_size = 64
        self.is_food = False
        self.food_bars = 0
        self.recipe = None

    def set_id(self, item_id: str):
        """
        Sets the items id
        """
        self.id = item_id
        return self

    def set_display_name(self, display_name: str):
        """
        Sets the items display name
        """
        self.display_name = display_name
        return self

    def set_texture_path(self, texture_path: str):
        """
        Sets the items texture path (if not provided, it will use default that uses id for file name in textures/items/id)
        """
        self.texture_path = texture_path
        return self

    def set_category(self, category: CreativeCategory):
        """
        Sets the items creative tab/category
        """
        self.category = category
        return self

    def set_max_stack_size(self, max_stack_size: int):
        """
        Set the max number the item can stack to
        """
        self.max_stack_size = max_stack_size
        return self

    def set_food(self, bars: int):
        """
        Sets is_food on the item and sets the value for the food consumption (food_bars)
        """
        self.is_food = True
        self.food_bars = bars
        return self

    def set_recipe(self, recipe: RecipeShaped | RecipeShapeless):
        """
        Sets the recipe for the item
        """
        self.recipe = recipe
        self.recipe.item_id = self.id
        return self

    def construct(self, namespace: str) -> dict:
        """
        Returns the item json used inside a behaviour pack
        """
        data = {
            "format_version": FORMAT_VERSION_ITEM,
            "minecraft:item": {
                "description": {
                    "identifier": f"{namespace}:{self.id}",
                    "category": self.category.value,
                },
                "components": {
                    "minecraft:icon": {"texture": f"{namespace}:{self.id}"},
                    "minecraft:display_name": {"value": self.display_name},
                    "minecraft:max_stack_size": self.max_stack_size,
                },
            },
        }

        if self.is_food:
            data["minecraft:item"]["components"]["minecraft:use_duration"] = 32
            data["minecraft:item"]["components"]["minecraft:food"] = {
                "nutrition": self.food_bars
            }

        return data


class RenderMethod(enum.Enum):
    BLEND = "blend"
    OPAQUE = "opaque"
    TRANSPARENT = "alpha_test"


class Block:
    """
    A minecraft bedrock block
    """

    id: str
    display_name: str
    texture_path: str | None
    category: CreativeCategory
    sound: BlockSounds

    hardness: int | float
    resistance: int
    render_method: RenderMethod

    recipe: RecipeShaped | RecipeShapeless | None

    def __init__(self) -> None:
        self.id = "placeholder"
        self.display_name = "Placeholder"
        self.texture_path = (
            None  # If None, it will use the default path that uses id as file name
        )
        self.category = CreativeCategory.CONSTRUCTION
        self.sound = BlockSounds.STONE
        self.hardness = 1
        self.resistance = 1
        self.render_method = RenderMethod.BLEND
        self.recipe = None

    def set_id(self, block_id: str):
        """
        Sets the blocks id
        """
        self.id = block_id
        return self

    def set_display_name(self, display_name: str):
        """
        Sets the blocks display name
        """
        self.display_name = display_name
        return self

    def set_texture_path(self, texture_path: str):
        """
        Sets the blocks texture path (if not provided, it will use default that uses id for file name in textures/blocks/id)
        """
        self.texture_path = texture_path
        return self

    def set_category(self, category: CreativeCategory):
        """
        Sets the blocks creative tab/category
        """
        self.category = category
        return self

    def set_sound(self, sound: BlockSounds):
        """
        Sets the blocks sound when walked on or used
        """
        self.sound = sound
        return self

    def set_hardness(self, hardness: int | float):
        """
        Sets the blocks hardness (how long it takes to break in seconds)
        """
        self.hardness = hardness
        return self

    def set_resistance(self, resistance: int):
        """
        Sets the blocks resistance (how much of a chance it will break from a explosion)
        """
        self.resistance = resistance
        return self

    def set_render_method(self, render_method: RenderMethod):
        """
        Sets the blocks rendering method (how it looks ingame, like if its transparent or opaque, etc..)
        """
        self.render_method = render_method
        return self

    def set_recipe(self, recipe: RecipeShaped | RecipeShapeless):
        """
        Sets the recipe for the block
        """
        self.recipe = recipe
        self.recipe.item_id = self.id
        return self

    def construct(self, namespace: str) -> dict:
        """
        Returns the block json used inside a behaviour pack
        """
        data = {
            "format_version": FORMAT_VERSION_BLOCK,
            "minecraft:block": {
                "description": {
                    "identifier": f"{namespace}:{self.id}",
                    "register_to_creative_menu": True,
                    "menu_category": {
                        "category": self.category.value,
                    },
                },
                "components": {
                    "minecraft:display_name": self.display_name,
                    "minecraft:material_instances": {
                        "*": {
                            "texture": f"{namespace}:{self.id}",
                            "render_method": self.render_method.value,
                        }
                    },
                    "minecraft:destructible_by_mining": {
                        "seconds_to_destroy": self.hardness
                    },
                    "minecraft:destructible_by_explosion": {
                        "explosion_resistance": self.resistance
                    },
                },
            },
        }

        return data


class Entity:
    """
    A minecraft bedrock entity
    """

    def __init__(self) -> None:
        pass

    def construct(self, namespace: str) -> dict[str, str]:
        """
        Returns the entity json used inside a behaviour pack
        """
        data = {}
        return data


class AddonManager:
    """
    Create Minecraft Bedrock Edition Addons using this class!
    """

    def __init__(
        self, name: str, description: str, namespace: str | None = None
    ) -> None:
        self.main_directory = OUT_DIRECTORY
        self.clean()

        self.name = name
        self.description = description

        technical_name = "_".join(self.name.lower().split(" "))
        self.namespace = technical_name if namespace is None else namespace

        self.behaviour_path = self.__ensure_file_or_folder_exists(
            path=OUT_DIRECTORY.joinpath(f"{technical_name}_behaviour"), is_folder=True
        )
        self.resource_path = self.__ensure_file_or_folder_exists(
            path=OUT_DIRECTORY.joinpath(f"{technical_name}_resources"), is_folder=True
        )

        self.items_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("items"), is_folder=True
        )
        self.items_textures_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/items"), is_folder=True
        )

        self.blocks_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("blocks"), is_folder=True
        )

        self.blocks_textures_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/blocks"), is_folder=True
        )

        self.recipes_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("recipes"), is_folder=True
        )

        self.items: list[Item] = []
        self.blocks: list[Block] = []
        self.entities: list[Entity] = []

        self.initalize()

    def __ensure_file_or_folder_exists(
        self, path: pathlib.Path, is_folder: bool = False
    ):
        """
        Checks if the path exists, if not it creates it and its parents
        """
        if not path.exists():
            if is_folder:
                path.mkdir(parents=True)
            else:
                path.touch()
        return path

    def __setup_behaviour_manifest(self, resource_manifest) -> dict:
        """
        Create and put the behaviour pack manifest into the addon
        """
        debug("Setting up behaviour manifest")

        manifest_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("manifest.json")
        )
        manifest = {
            "format_version": FORMAT_VERSION,
            "header": {
                "name": f"{self.name} Behaviour",
                "description": self.description,
                "uuid": str(uuid.uuid4()),
                "version": GLOBAL_VERSION,
                "min_engine_version": MIN_ENGINE_VERSION,
            },
            "modules": [
                {
                    "description": self.description,
                    "type": "data",
                    "uuid": str(uuid.uuid4()),
                    "version": GLOBAL_VERSION,
                }
            ],
            "dependencies": [
                {
                    "uuid": resource_manifest["header"]["uuid"],
                    "version": resource_manifest["header"]["version"],
                }
            ],
        }

        manifest_path.write_text(json.dumps(manifest, indent=4))
        return manifest

    def __setup_resources_manifest(self) -> dict:
        """
        Create and put the resource pack manifest into the addon
        """
        debug("Setting up resources manifest")

        manifest_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("manifest.json")
        )
        manifest = {
            "format_version": FORMAT_VERSION,
            "header": {
                "name": f"{self.name} Resources",
                "description": self.description,
                "uuid": str(uuid.uuid4()),
                "version": GLOBAL_VERSION,
                "min_engine_version": MIN_ENGINE_VERSION,
            },
            "modules": [
                {
                    "description": self.description,
                    "type": "resources",
                    "uuid": str(uuid.uuid4()),
                    "version": GLOBAL_VERSION,
                }
            ],
        }

        manifest_path.write_text(json.dumps(manifest, indent=4))
        return manifest

    def clean(self):
        """
        reset/clear the contents in the out folder
        """
        shutil.rmtree(self.main_directory)
        self.main_directory.mkdir()

    def __write_to_lang(self, key: str, value: str):
        """
        Write the item (id) display name to texts/(language).json
        """
        # TODO: other languages?
        default_lang = "en_US"
        debug(f"Writing '{key}' to language {default_lang} with value '{value}'")
        lang_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("texts"), is_folder=True
        )
        lang_file_path = self.__ensure_file_or_folder_exists(
            path=lang_path.joinpath(f"{default_lang}.lang")
        )
        lang_text = lang_file_path.read_text().lstrip()
        lang_file_path.write_text(f"{lang_text}\n{key}={value}")

    def __write_item_texture(self, item: Item):
        """
        Write the item (item.id) texture to textures/item_texture.json
        """
        item_textures_json_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/item_texture.json")
        )
        name = f"{self.namespace}:{item.id}"
        try:
            parsed = json.loads(item_textures_json_path.read_text())
            parsed["texture_data"][name] = {
                "textures": f"textures/items/{item.id}"
                if item.texture_path is None
                else item.texture_path
            }
            item_textures_json_path.write_text(json.dumps(parsed, indent=4))
        except:
            item_textures_json_path.write_text(
                json.dumps(
                    {
                        "texture_name": "atlas.items",
                        "texture_data": {
                            name: {
                                "textures": f"textures/items/{item.id}"
                                if item.texture_path is None
                                else item.texture_path
                            }
                        },
                    },
                    indent=4,
                )
            )
        debug(f"Make sure to provide the texture for item with id '{item.id}'")

    def __write_block_sound(self, block: Block):
        blocks_resource_sounds_json_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("blocks.json")
        )
        name = f"{self.namespace}:{block.id}"
        try:
            parsed = json.loads(blocks_resource_sounds_json_path.read_text())
            parsed[name] = {"sound": block.sound.value, "textures": block.texture_path}
            blocks_resource_sounds_json_path.write_text(json.dumps(parsed, indent=4))
        except:
            data = {
                "format_version": FORMAT_VERSION_BLOCK_SOUND,
                name: {"sound": block.sound.value, "textures": name},
            }
            blocks_resource_sounds_json_path.write_text(json.dumps(data, indent=4))

    def __write_block_texture(self, block: Block):
        """
        Write the block (block.id) texture to textures/terrain_texture.json
        """
        block_textures_json_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/terrain_texture.json")
        )
        name = f"{self.namespace}:{block.id}"
        try:
            parsed = json.loads(block_textures_json_path.read_text())
            parsed["texture_data"][name] = {
                "textures": f"textures/blocks/{block.id}"
                if block.texture_path is None
                else block.texture_path
            }
            block_textures_json_path.write_text(json.dumps(parsed, indent=4))
        except:
            block_textures_json_path.write_text(
                json.dumps(
                    {
                        "texture_name": "atlas.terrain",
                        "padding": 8,
                        "num_mip_levels": 4,
                        "texture_data": {
                            name: {
                                "textures": f"textures/blocks/{block.id}"
                                if block.texture_path is None
                                else block.texture_path
                            }
                        },
                    },
                    indent=4,
                )
            )
        debug(f"Make sure to provide the texture for block with id '{block.id}'")

    def add_item(self, item: Item):
        """
        Add a custom item to the addon using the Item class
        """
        debug(f"Adding item with id '{item.id}'")
        index = len(self.items)
        self.items.append(item)
        return index

    def add_block(self, block: Block):
        """
        Add a custom block to the addon using the Block class
        """
        debug(f"Adding block with id '{block.id}'")
        index = len(self.blocks)
        self.blocks.append(block)
        return index

    def __real_initalize(self):
        rp_manifest = self.__setup_resources_manifest()
        self.__setup_behaviour_manifest(rp_manifest)
        debug("Finished initalizing\n")

    def initalize(self):
        """
        Initalize Addon Manager
        """
        try:
            self.__real_initalize()
        except Exception as err:
            error(f"Failed to initalize AddonManager: {err}")

    def __generate_recipe(self, recipe: RecipeShaped | RecipeShapeless | None):
        if recipe is None:
            return
        recipe_json_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath(f"recipes/{recipe.item_id}.json"),
        )
        recipe_json_path.write_text(
            json.dumps(recipe.construct(self.namespace), indent=4)
        )

    def __generate_items(self):
        for item in self.items:
            self.__write_to_lang(
                key=f"item.{self.namespace}:{item.id}.name", value=item.display_name
            )
            self.__write_item_texture(item)
            self.__generate_recipe(item.recipe)
            item_path = self.__ensure_file_or_folder_exists(
                path=self.items_behaviour_path.joinpath(f"{item.id}.json")
            )
            item_data = item.construct(self.namespace)
            item_path.write_text(json.dumps(item_data, indent=4))

    def __generate_blocks(self):
        for block in self.blocks:
            self.__write_to_lang(
                key=f"tile.{self.namespace}:{block.id}.name", value=block.display_name
            )
            self.__write_block_texture(block)
            self.__write_block_sound(block)
            self.__generate_recipe(block.recipe)
            block_path = self.__ensure_file_or_folder_exists(
                path=self.blocks_behaviour_path.joinpath(f"{block.id}.json")
            )
            block_data = block.construct(self.namespace)
            block_path.write_text(json.dumps(block_data, indent=4))

    def generate(self):
        """
        Generate the files for the addon like items, blocks, recipes, etc...
        """
        self.__generate_items()
        self.__generate_blocks()
