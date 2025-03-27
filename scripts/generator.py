import ast
from rich import print
import os
from pathlib import Path
import re
import json
import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from typing import Dict, Any, Optional, List
from aea.cli.utils.click_utils import PublicId

console = Console()

def validate_type(value: str, var_type: str) -> bool:
    """
    Validate input against specified type.
    
    :param value: Input value as string
    :param var_type: Expected type (str, int, bool, list, json)
    :return: Type validation result
    """
    try:
        if var_type == 'str':
            return isinstance(value, str)
        elif var_type == 'int':
            int(value)
            return True
        elif var_type == 'float':
            float(value)
            return True
        elif var_type == 'bool':
            return value.lower() in ['true', 'false']
        elif var_type == 'list':
            return (value.startswith('[') and value.endswith(']')) or \
                   (isinstance(ast.literal_eval(value), list))
        elif var_type == 'json':
            json.loads(value)
            return True
        return False
    except (ValueError, json.JSONDecodeError, SyntaxError):
        return False


def check_file_presence(file_paths: List[str]) -> List[str]:
    """
    Validate presence of multiple files.
    
    :param file_paths: List of file paths to check
    :return: List of missing files
    """
    return [path for path in file_paths if not os.path.exists(path)]

def parse_config(config_content: str) -> Dict[str, Dict[str, Any]]:
    TYPES = {"str", "int", "bool", "float", "list", "dict"}

    # Match: ${[var:]type:default}
    pattern = r"\${(?:(\w+):)?(\w+):([^}]+)}"

    def parse_match(var, typ, default):
        # case where all three are present
        if var in TYPES:
            default = ":".join([typ, default])
            return {"var": None, "type": var, "default": default}
        # case where type and default are present
        if var and typ and default:
            return {"var": var, "type": typ, "default": default}
        # case where var and type are present
        if var and typ:
            return {"var": var, "type": typ, "default": None}
        
        if typ and default:
            return {"var": None, "type": typ, "default": default}
    matches = re.findall(pattern, config_content)
    return [parse_match(*m) for m in matches]




@click.command()
@click.argument('public_id', type=PublicId.from_str, required=True)
@click.option('--output', default='.env', help='Output .env file path', type=click.Path())
@click.option('--type', default='agent', help='Type of package to generate the .env file for.', type=click.Choice(['agent', 'service']))
@click.option('--show-config', is_flag=True, help='Show the configuration file contents')
def generate_env_vars(public_id: PublicId, output: str, type: str, show_config: bool):
    """
    Interactive environment variable configuration generator.
    
    :param config: Configuration file path
    :param output: Output .env destination
    """

    from auto_dev.utils import load_autonolas_yaml
    from aea.configurations.constants import AGENT, SERVICE, DEFAULT_SERVICE_CONFIG_FILE, DEFAULT_AEA_CONFIG_FILE

    # We detect if it is a service or an agent

    if type == 'agent':
        name_key = "agent_name"
    elif type == 'service':
        name_key = "name"
    else:
        click.echo("Invalid package type. Must be either 'agent' or 'service'.")
        click.Abort()
    config_dir = f"packages/{public_id.author}/{type}s/{public_id.name}"
    config_path = Path(config_dir) / DEFAULT_AEA_CONFIG_FILE if type == AGENT else Path(config_dir) / DEFAULT_SERVICE_CONFIG_FILE
    config_yaml, *overrides = load_autonolas_yaml(
        package_type=type,
        directory=Path(config_dir),
    )

    author, name = config_yaml['author'], config_yaml[name_key]

    console.print(Panel.fit(f"[bold green]Olas Agent Env Configurator for {type}: {author}/{name} [/bold green]"))
    
    if Path(output).exists():
        click.confirm(f"File {output} already exists. Overwrite?", abort=True)
        if show_config:
            console.print(Panel(
                Syntax(config_path.read_text(), "yaml"),
                title="[bold green]Configuration File[/bold green]"
            ))


    try:
        required_vars = parse_config(Path(config_path).read_text())
    except FileNotFoundError:
        return
    
    env_contents = []
    to_set = []
    print()
    print("Necessary Environment Variables To Be Set:")
    print()
    for var_info in required_vars:

        var_name = var_info['var']
        var_type = var_info['type']
        var_default = var_info['default']

        if var_name and var_type and var_default:
            to_set.append([var_name, var_type, var_default])
            print(f"    {var_name}")
        if not var_default:
            to_set.append([var_name, var_type, var_default])
    print()
    print("Please input the required environment variables.")
    for var_name, var_type, var_default in to_set:
        print()
        print(f"     [bold]{var_name}[/bold]            (type: {var_type} example: {var_default})")
        while True:
            value = click.prompt(
                "Please enter a value",
                hide_input=False
            )

            if validate_type(value, var_type):
                break
            console.print(f"[bold red]Invalid type. Expected {var_type}[/bold red]")
        env_contents.append(f"{var_name}={value}")

    
    with open(output, 'w') as f:
        f.write('\n'.join(env_contents))
    
    console.print(Panel(
        Syntax('\n'.join(env_contents), "ini"),
        title="[bold green]Generated .env File[/bold green]"
    ))
    
    console.print(f"[bold green]✓[/bold green] Environment variables written to {output}")

if __name__ == '__main__':
    generate_env_vars()