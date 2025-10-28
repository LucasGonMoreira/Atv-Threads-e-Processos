import pandas as pd
import os
import multiprocessing
import threading
import time


dado = pd.read_csv('atividade threads\dadosInep.csv')



contador_global = 0

def tarefa_thread():
    inicio = time.time() #Adiciona o tempo inicial para calcular o tempo de execução

    global contador_global # Variável Global compartilhada entre threads
    
    pid = os.getpid() # ID do Processo
    thread_id = threading.get_ident() # Pega o ID da Thread atual
    
    print(f"\n[PROCESSO | PID: {pid} | TID: {thread_id}] INICIADA.") 
    
    
    contador_global += 10 # Altera a variável global
    
    df_fem = dado['MEDIA_NOTAS'][dado['TP_SEXO'] == 'M'] #Filtra os dados para sexo masculino
    print(df_fem.median(), "M") #Imprime a mediana das notas masculinas

    df_fem = dado['MEDIA_NOTAS'][dado['TP_SEXO'] == 'F'] #Filtra os dados para sexo feminino
    print(df_fem.median(), "F") #Imprime a mediana das notas femininas

    tempo = time.time() - inicio #Calcula o tempo de execução da thread

    print(f"[THREAD | PID: {pid} | TID: {thread_id}] Contador alterado para: {contador_global} tempo foi {tempo}" )


def tarefa_processo():
    inicio = time.time() #Adiciona o tempo inicial para calcular o tempo de execução

    global contador_global # Variável Global (cópia isolada para cada processo)
    
    pid = os.getpid() # ID do Processo
    
    print(f"\n[PROCESSO | PID: {pid}] INICIADO.") #Processo iniciado
    
    contador_global += 100 # Altera a variável global (cópia local do processo)

    df_fem = dado['MEDIA_NOTAS'][dado['TP_SEXO'] == 'M'] #Filtra os dados para sexo masculino
    print(df_fem.median(), "M") #Imprime a mediana das notas masculinas

    df_fem = dado['MEDIA_NOTAS'][dado['TP_SEXO'] == 'F'] #Filtra os dados para sexo feminino
    print(df_fem.median(), "F")   #Imprime a mediana das notas femininas

    tempo = time.time() - inicio #Calcula o tempo de execução da thread
    

    print(f"[PROCESSO | PID: {pid}] Contador local alterado para: {contador_global} o tempo foi {tempo}")


if __name__ == '__main__':
    
    print("="*50)
    print("Valor inicial do Contador Global (MAIN):", contador_global)
    print("PID do Processo Principal (MAIN):", os.getpid())
    print("="*50)

    # --- TESTE 1: THREADS ---
    
    # 1. Cria e inicia a Thread
    t = threading.Thread(target=tarefa_thread)
    t.start()
    t.join() # Espera a thread terminar
    
    print("-" * 50)
    print("RESULTADO THREAD:")
    print(f"Valor FINAL do Contador Global (MAIN): {contador_global}")
    print("-> A thread alterou o valor com sucesso! (Compartilhamento de Memória)")
    print("-" * 50)

    # --- TESTE 2: PROCESSOS ---
    
    # 2. Reseta o contador global para o próximo teste
    #contador_global = 0 
    print(f"\nValor resetado para: {contador_global}")
    
    # 3. Cria e inicia o Processo
    p = multiprocessing.Process(target=tarefa_processo)
    p.start()
    p.join() # Espera o processo terminar
    
    print("-" * 50)
    print("RESULTADO PROCESSO:")
    print(f"Valor FINAL do Contador Global (MAIN): {contador_global}")
    print("-> O processo NÃO alterou o valor! (Memória Isolada)")
    print("-" * 50)