class VueHandler:
    @staticmethod
    def suggest_path(component_name: str) -> str:
        return f"src/components/{component_name}.vue"

    @staticmethod
    def get_boilerplate(name: str) -> str:
        return f"<template>\n  <div class='{name}'></div>\n</template>\n<script setup>\n</script>"