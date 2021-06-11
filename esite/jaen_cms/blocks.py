from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from bifrost.api.helpers import register_streamfield_block
from bifrost.api.models import (
    GraphQLCollection,
    GraphQLEmbed,
    GraphQLForeignKey,
    GraphQLImage,
    GraphQLString,
)


class StreamFieldBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(classname="full title")
    subheading = blocks.RichTextBlock()

    graphql_fields = [GraphQLString("heading"), GraphQLString("subheading")]
