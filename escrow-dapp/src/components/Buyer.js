import React from 'react';
import { ThanosWallet } from "@thanos-wallet/dapp";

export default class setbuyer extends React.Component {
  constructor(props){
    super(props)
    this.state = { price: null}
  };

  async buying() {
    try {
        const available = await ThanosWallet.isAvailable();
        if (!available) {
          throw new Error("Thanos Wallet not installed");
        }

        const wallet = new ThanosWallet("Escrow");
        const connect = await wallet.connect("carthagenet", { forcePermission: true });
        const tezos = wallet.toTezos();

        const accountPkh = await tezos.wallet.pkh();
        const accountBalance = await tezos.tz.getBalance(accountPkh);
        console.info(`address: ${accountPkh}, balance: ${accountBalance}`);
        const price=this.state.price

        const buy = await tezos.wallet.at("KT1Hwvkf7vioVtDj7FbPfhWGQTnQe3FGmmyu");
        const operation = await buy.methods.setBuyer(Symbol()).send({ amount: 2*price, mutez: true});
        const transtat = await operation.confirmation();
        alert(transtat);

        const contractstorage = await buy.storage();
        console.info(`Storage: ${contractstorage}`);
      } catch (err) {
        console.error(err);
      }
  }

  render() {
    return(
      <div className="mainContainer">
        <h1>Buy a Guitar</h1>
        <label>Enter the buying price of the guitar : </label>
        <input type="number" className="inputStyle" placeholder="0" step="1" value={this.state.price} onChange={ (eve) => { this.setState({ price: Number(eve.target.value) }) } }/>
        <br/><br/>
        <button onClick={()=>{this.buying()}} >Buy Guitar</button>

        <br/><br/>
      </div>
    )
  }
}
