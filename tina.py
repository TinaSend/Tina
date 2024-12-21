import asyncio
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.publickey import PublicKey
from solana.system_program import TransferParams, transfer
from solana.keypair import Keypair
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
import json

class TinaAgent:
    def __init__(self, rpc_url: str, program_id: str):
        self.client = AsyncClient(rpc_url)
        self.program_id = PublicKey(program_id)

    async def get_account_info(self, public_key: str):
        """Fetch account information from the Solana blockchain."""
        response = await self.client.get_account_info(PublicKey(public_key))
        return response

    async def send_transaction(self, sender: Keypair, recipient: str, lamports: int):
        """Send a transaction on the Solana blockchain."""
        transaction = Transaction()
        transaction.add(
            transfer(
                TransferParams(
                    from_pubkey=sender.public_key,
                    to_pubkey=PublicKey(recipient),
                    lamports=lamports,
                )
            )
        )
        try:
            response = await self.client.send_transaction(
                transaction, sender, opts=TxOpts(preflight_commitment=Confirmed)
            )
            return response["result"]
        except Exception as e:
            print(f"Error sending transaction: {e}")
            return None

    async def interact_with_smart_contract(self, account: Keypair, instruction_data: dict):
        """Send instructions to a smart contract."""
        transaction = Transaction()
        transaction.add(
            transfer(
                TransferParams(
                    from_pubkey=account.public_key,
                    to_pubkey=self.program_id,
                    lamports=0,  # Fee for interacting with the smart contract
                )
            )
        )
        try:
            encoded_data = json.dumps(instruction_data).encode("utf-8")
            transaction.add_instruction(encoded_data)
            response = await self.client.send_transaction(
                transaction, account, opts=TxOpts(preflight_commitment=Confirmed)
            )
            return response["result"]
        except Exception as e:
            print(f"Error interacting with smart contract: {e}")
            return None

    async def close(self):
        """Close the connection to the Solana RPC client."""
        await self.client.close()

# Example Usage
async def main():
    # Initialize TinaAgent with the RPC URL and program ID
    rpc_url = "https://api.mainnet-beta.solana.com"
    program_id = "PROGRAM_ID_HERE"
    tina_agent = TinaAgent(rpc_url, program_id)

    # Fetch account information
    public_key = "ACCOUNT_PUBLIC_KEY"
    account_info = await tina_agent.get_account_info(public_key)
    print("Account Info:", account_info)

    # Send a transaction
    sender_keypair = Keypair()  # Replace with your sender's keypair
    recipient = "RECIPIENT_PUBLIC_KEY"
    lamports = 1000000  # Replace with the amount to send
    transaction_result = await tina_agent.send_transaction(sender_keypair, recipient, lamports)
    print("Transaction Result:", transaction_result)

    # Interact with a smart contract
    instruction_data = {"action": "update_data", "payload": {"key": "value"}}
    smart_contract_result = await tina_agent.interact_with_smart_contract(sender_keypair, instruction_data)
    print("Smart Contract Result:", smart_contract_result)

    # Close connection
    await tina_agent.close()

# Run the main event loop
if __name__ == "__main__":
    asyncio.run(main())
