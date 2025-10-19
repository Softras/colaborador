import sqlite3
import pandas as pd
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="colaboradores.db"):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """Cria a tabela de colaboradores se não existir"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS colaboradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                endereco TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                cep TEXT,
                telefone TEXT,
                data_nascimento DATE,
                cargo TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def inserir_colaborador(self, dados):
        """Insere um novo colaborador no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO colaboradores 
            (nome_completo, endereco, bairro, cidade, estado, cep, telefone, data_nascimento, cargo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def listar_colaboradores(self):
        """Lista todos os colaboradores"""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM colaboradores ORDER BY id DESC", conn)
        conn.close()
        return df
    
    def buscar_colaborador_por_id(self, id_colaborador):
        """Busca um colaborador específico pelo ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colaboradores WHERE id = ?", (id_colaborador,))
        colaborador = cursor.fetchone()
        conn.close()
        return colaborador
    
    def atualizar_colaborador(self, id_colaborador, dados):
        """Atualiza os dados de um colaborador"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE colaboradores 
            SET nome_completo=?, endereco=?, bairro=?, cidade=?, estado=?, 
                cep=?, telefone=?, data_nascimento=?, cargo=?
            WHERE id=?
        """, dados + (id_colaborador,))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def excluir_colaborador(self, id_colaborador):
        """Exclui um colaborador pelo ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM colaboradores WHERE id = ?", (id_colaborador,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def contar_colaboradores(self):
        """Retorna o número total de colaboradores"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM colaboradores")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def obter_estatisticas(self):
        """Retorna estatísticas básicas do banco"""
        df = self.listar_colaboradores()
        
        if df.empty:
            return {
                'total_colaboradores': 0,
                'total_cidades': 0,
                'total_estados': 0,
                'total_cargos': 0,
                'cargo_mais_comum': 'N/A',
                'estado_mais_comum': 'N/A'
            }
        
        stats = {
            'total_colaboradores': len(df),
            'total_cidades': df['cidade'].nunique() if not df['cidade'].isna().all() else 0,
            'total_estados': df['estado'].nunique() if not df['estado'].isna().all() else 0,
            'total_cargos': df['cargo'].nunique() if not df['cargo'].isna().all() else 0,
            'cargo_mais_comum': df['cargo'].mode().iloc[0] if not df['cargo'].isna().all() and len(df['cargo'].mode()) > 0 else 'N/A',
            'estado_mais_comum': df['estado'].mode().iloc[0] if not df['estado'].isna().all() and len(df['estado'].mode()) > 0 else 'N/A'
        }
        
        return stats