import React from 'react';
import { ThanosWallet } from "@thanos-wallet/dapp";

export default class refundbuyer extends React.Component {
  constructor(props){
    super(props)
    this.state = { price: 0}
  };

  async cancel() {
    try {
        const available = await ThanosWallet.isAvailable();
        if (!available) {
          throw new Error("Thanos Wallet not installed");
        }

        const wallet = new ThanosWallet("Escrow");
        await wallet.connect("carthagenet", { forcePermission: true });
        const tezos = wallet.toTezos();

        const accountPkh = await tezos.wallet.pkh();
        const accountBalance = await tezos.tz.getBalance(accountPkh);
        console.info(`address: ${accountPkh}, balance: ${accountBalance}`);

        const cancel = await tezos.wallet.at("KT1Hwvkf7vioVtDj7FbPfhWGQTnQe3FGmmyu");
        const operation = await cancel.methods.refundBuyer(Symbol()).send();
        const transtat=await operation.confirmation();
        alert(transtat);

        const counterValue = await cancel.storage();
        console.info(`Storage: ${counterValue}`);
        console.info(`Result: ${operation}`);
      } catch (err) {
        console.error(err);
      }
  }

  render() {
    return(
      <div className="mainContainer">
        <h1>Cancel the sell order you have initiated</h1>
        <br/><br/>
        <button onClick={()=>{this.cancel()}} >Cancel your sell Order</button>

        <br/><br/>
      </div>
    )
  }
}
