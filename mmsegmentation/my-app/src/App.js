import './App.css';
import { useState } from 'react';
import Userinfo from "./component/Userinfo"
import UploadImage from "./component/UploadImage"
import InferenceResult from "./component/InferenceResult"
import Message from './component/Message';

function App() {  
  const [userInfoView, setUserInfoView] = useState(false);

  return (
    <div className="page">
      <Userinfo disabled={true}/>
      <br></br>
      <UploadImage />
      <br></br>
      <InferenceResult />
    </div>
  );
  
}


export default App;
