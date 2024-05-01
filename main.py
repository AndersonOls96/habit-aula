import flet as ft
import sqlite3

def init_db():
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL CHECK (done IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()
    
def fetch_habits():
    # Conectar ao banco de dados
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    # Executar a consulta SQL
    cursor.execute('SELECT id, title, done FROM habits')
    
    # Buscar todos os resultados
    habits_list = cursor.fetchall()
    
    # Fechar a conexão com o banco de dados
    conn.close()
    
    # Retornar os resultados
    return habits_list
    

def main(page: ft.Page):
    page.bgcolor = ft.colors.BLACK
    page.padding = ft.padding.all(30)
    page.window_resizable = False
    page.window_height = 960
    page.window_width = 600
    
    init_db()

    habits_list = fetch_habits()
    
    
    
    def delete_habit(e, habit_id):
        # Conectar ao banco de dados
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        
        # Excluir o hábito pelo ID
        cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        
        # Salvar as mudanças e fechar a conexão
        conn.commit()
        conn.close()
        
        # Atualizar a UI
        refresh_habits_ui()
    
    
    def edit_habit(e, habit_id):
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
    
        # Encontrar o hábito pelo ID
        cursor.execute('SELECT id, title, done FROM habits WHERE id = ?', (habit_id,))
        habit = cursor.fetchone()
            
        if habit is not None:
            # Substitui o Checkbox e o IconButton pelo TextField para edição.
            index = habits_list.index(habit)
            habits.content.controls[index] = ft.Row(
                controls=[
                    ft.TextField(
                        value=habit[1],
                        on_submit=lambda e, hl=habit_id: update_habit_title(e, hl),
                        autofocus=True,
                    )
                ]
            )
            habits.update()

    def update_habit_title(e, habit):
            # Conectar ao banco de dados
            conn = sqlite3.connect('habits.db')
            cursor = conn.cursor()
            
            # Atualizar o título do hábito com base no seu ID
            new_title = e.control.value
            cursor.execute('UPDATE habits SET title = ? WHERE id = ?', (new_title, habit))
            
            # Salvar as mudanças
            conn.commit()
            
            # Fechar a conexão com o banco de dados
            conn.close()
            
            # Atualizar a UI após a mudança
            refresh_habits_ui()

    def refresh_habits_ui():
        # Obter os hábitos do banco de dados
        habits_list = fetch_habits()
        
        # Atualizar a interface do usuário com os novos dados
        habits.content.controls = [
            ft.Row(
                controls=[
                    ft.Checkbox(
                        label=hl[1],  # habit[1] é o título do hábito
                        value=bool(hl[2]),  # habit[2] é o status 'done', convertido para bool
                        on_change=lambda e, id=hl[0]: change(e, id)  # Adicione a lógica de mudança aqui
                    ),
                    ft.IconButton(
                        icon=ft.icons.EDIT,
                        icon_color=ft.colors.BLACK,
                        on_click=lambda e, id=hl[0]: edit_habit(e, id)  # Implemente a lógica de edição aqui
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color=ft.colors.BLACK,
                        on_click=lambda e, id=hl[0]: delete_habit(e, id)  # Implemente a lógica de exclusão aqui
                    ) 
                ]
            ) for hl in habits_list
        ]
        habits.update()

    def change(e, habit_id):
        # Conectar ao banco de dados
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        
        # Atualizar o status 'done' do hábito com base no seu 'id'
        new_status = 1 if e.control.value else 0  # Convertendo o valor para 1 (True) ou 0 (False)
        cursor.execute('UPDATE habits SET done = ? WHERE id = ?', (new_status, habit_id))
        
        # Salvar as mudanças
        conn.commit()
        
        # Fechar a conexão com o banco de dados
        conn.close()
        
        # Atualizar a UI após a mudança
        update_progress()
        refresh_habits_ui()
        
    def update_progress():
        # Conectar ao banco de dados
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        
        # Buscar todos os hábitos
        cursor.execute('SELECT done FROM habits')
        habits_list = cursor.fetchall()
        
        # Calcular o progresso
        done = sum(habit[0] for habit in habits_list)
        total = len(habits_list)
        progress = done / total if total > 0 else 0  # Evitar divisão por zero
        
        # Atualizar os controles de progresso na UI
        progress_bar.value = f'{progress:.2f}'
        progress_text.value = f'{progress:.0%}'
        progress_bar.update()
        progress_text.update()
        
        # Fechar a conexão com o banco de dados
        conn.close()

    def add_habit(e):
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO habits (title, done) VALUES (?, ?)', (e.control.value, 0))
        conn.commit()
        conn.close()
        refresh_habits_ui()
        e.control.value = ''
        e.control.update()

    layout = ft.Column(
        expand=True,
        controls=[
            ft.Text(value='Que bom ter você aqui', size=30, color=ft.colors.WHITE),
            ft.Text(value='Como estão seus hábitos hoje?', size=20, color=ft.colors.GREY),

            ft.Container(
                padding=ft.padding.all(30),
                bgcolor=ft.colors.INDIGO,
                border_radius=ft.border_radius.all(20),
                margin=ft.margin.symmetric(vertical=30),
                content=ft.Column(
                    controls=[
                        ft.Text(value='Sua evolução hoje', size=20, color=ft.colors.WHITE),
                        progress_text := ft.Text(value='0%', size=50, color=ft.colors.WHITE),
                        progress_bar := ft.ProgressBar(
                            value=0, 
                            color=ft.colors.INDIGO_900, 
                            bgcolor=ft.colors.INDIGO_100,
                            height=20,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            
            ft.Text(value='Hábitos de hoje', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Text(value='Marcar suas tarefas como concluído te motiva a continuar focado.', size=16, color=ft.colors.WHITE),

            habits := ft.Container(
                expand=True,
                padding=ft.padding.all(30),
                bgcolor=ft.colors.GREY_300,
                border_radius=ft.border_radius.all(20),
                margin=ft.margin.symmetric(vertical=20),
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=20,
                     controls=[
                        ft.Row(
                            controls = [
                                ft.Checkbox(
                                    label=hl[1], 
                                    value=hl[2], 
                                    on_change=lambda e, id=hl[0]: change(e, id)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.BLACK,
                                     on_click=lambda e, id=hl[0]: edit_habit(e, id)
                                    
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.BLACK,
                                    on_click=lambda e, id=hl[0]: delete_habit(e, id)
                                )    
                            ]
                        )for hl in habits_list
                    ]
                ),
            ),
            
            ft.Text(value='Adicionar novo hábito', size=20, color=ft.colors.WHITE),
            ft.TextField(
                hint_text='Escreva um hábito...',
                bgcolor = ft.colors.WHITE,
                border=ft.InputBorder.UNDERLINE,
                on_submit=add_habit
            )
        ]
    )

    page.add(layout)

if __name__ == '__main__':
    ft.app(target=main)