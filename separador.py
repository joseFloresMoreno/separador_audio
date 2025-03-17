from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich import print as rprint

console = Console()

def split_audio(audio_path, silence_len, silence_thresh):
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
        ) as progress:
            # Cargar el audio
            task = progress.add_task("[cyan]Cargando audio...", total=None)
            audio = AudioSegment.from_file(audio_path)
            progress.update(task, completed=True)

            # Detectar segmentos no silenciosos
            task = progress.add_task("[cyan]Detectando segmentos...", total=None)
            segments = split_on_silence(
                audio,
                min_silence_len=silence_len,  # tiempo de silencio personalizado
                silence_thresh=silence_thresh, # umbral de silencio personalizado
                keep_silence=200        # mantener 100ms de silencio al inicio y final
            )
            progress.update(task, completed=True)

            # Crear directorio de salida
            output_dir = os.path.join(os.path.dirname(audio_path), "segmentos")
            os.makedirs(output_dir, exist_ok=True)

            # Exportar segmentos
            task = progress.add_task("[cyan]Exportando segmentos...", total=len(segments))
            for i, segment in enumerate(segments):
                output_path = os.path.join(output_dir, f"audio_{i+1}.mp3")
                segment.export(output_path, format="mp3")
                progress.advance(task)

        rprint("[green]¡Proceso completado![/green]")
        rprint(f"[blue]Se han creado {len(segments)} segmentos en la carpeta: {output_dir}[/blue]")

    except Exception as e:
        rprint(f"[red]Error: {str(e)}[/red]")

def main():
    try:
        console.print("[bold blue]Separador de Audio[/bold blue]")
        console.print("[yellow]Este script separará el audio en segmentos basados en silencios de 1 segundo[/yellow]\n")
        
        audio_path = console.input("[cyan]Por favor, ingrese la ruta del archivo de audio: [/cyan]")
        
        if not os.path.exists(audio_path):
            rprint("[red]¡Error! La ruta del archivo no existe.[/red]")
            return
        
        # Nuevos inputs para los parámetros
        while True:
            try:
                silence_len = int(console.input("[cyan]Ingrese el tiempo mínimo de silencio en milisegundos (recomendado 1000): [/cyan]"))
                if silence_len <= 0:
                    rprint("[red]El tiempo debe ser mayor a 0[/red]")
                    continue
                break
            except ValueError:
                rprint("[red]Por favor ingrese un número válido[/red]")

        while True:
            try:
                silence_thresh = int(console.input("[cyan]Ingrese el umbral de silencio en dB (recomendado -40): [/cyan]"))
                break
            except ValueError:
                rprint("[red]Por favor ingrese un número válido[/red]")
        
        split_audio(audio_path, silence_len, silence_thresh)
    except KeyboardInterrupt:
        rprint("\n[yellow]Proceso cancelado por el usuario[/yellow]")
    except Exception as e:
        rprint(f"[red]Error inesperado: {str(e)}[/red]")
    finally:
        input("\nPresione Enter para salir...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        rprint(f"[red]Error crítico: {str(e)}[/red]")
        input("\nPresione Enter para salir...")
