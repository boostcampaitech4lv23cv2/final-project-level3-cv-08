import './App.css';
import { useState, useRef, useEffect } from 'react';
import InputWithLabel from './component/InputWithLabel';
import SelectWithLabel from './component/SelectWithLabel';
import carFrontPrev from './images/carFront.png'
import carBackPrev from './images/carBack.png'
import carLeftPrev from './images/carLeft.png'
import carRightPrev from './images/carRight.png'

function App() {  
  const [userName, setuserName] = useState("");
  const [carNum, setcarNum] = useState();
  const [userPhone, setuserPhone] = useState();
  const [userRent, setuserRent] = useState();

  const [userNameValid, setUserNameValid] = useState(false);
  const [carNumValid, setCarNumValid] = useState(false);
  const [userPhoneValid, setUserPhoneValid] = useState(false);

  const [disabledUserinfo, setDisabledUserinfo] = useState("");
  const [allowUserinfo, setAllowUserinfo] = useState(true);
  const [loadingUserinfo, setLoadingUserinfo] =useState("none");

  const [carFrontImg, setCarFrontImg] = useState("");
  const [carBackImg, setCarBackImg] = useState("");
  const [carLeftImg, setCarLeftImg] = useState("");
  const [carRightImg, setCarRightImg] = useState("");

  const [carFrontState, setCarFrontState] = useState(false);
  const [carBackState, setCarBackState] = useState(false);
  const [carLeftState, setCarLeftState] = useState(false);
  const [carRightState, setCarRightState] = useState(false);

  const [carFrontRes, setCarFrontRes] = useState("");
  const [carBackRes, setCarBackRes] = useState("");
  const [carLeftRes, setCarLeftRes] = useState("");
  const [carRightRes, setCarRightRes] = useState("");

  const [uploadingImg, setUploadingImg] = useState("none");

  const carFrontRef = useRef();
  const carBackRef = useRef();
  const carLeftRef = useRef();
  const carRightRef = useRef();

  const onChangeuserName = (event) => {
    setuserName(event.target.value);
    setUserNameValid(true);
  }
  const onChangecarNum = (event) => {
    setcarNum(event.target.value);
    setCarNumValid(true);
  }
  const onChangeuserPhone = (event) => {
    setuserPhone(event.target.value);
    setUserPhoneValid(true);
  }
  const onChangeuserRent = (event) => {
    setuserRent(event.target.value);
  }

  useEffect(() => {
    if (userNameValid && carNumValid && userPhoneValid){
      setAllowUserinfo(false);
    }

  })

  const onSubmitClick = (event) => {
    event.preventDefault();
      if (userName === "" | carNum === "" | userPhone === ""){
          return;
      }
      else {
        setLoadingUserinfo("");
        setDisabledUserinfo("true");
        // console.log("사용자 정보가 click!!!!");
        alert(`${userName}님 반갑습니다!`);
      }      
  }

  const saveCarFrontImg = () => {
    const file = carFrontRef.current.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
        setCarFrontImg(reader.result);
    };
    setCarFrontState(true);
};

  const saveCarBackImg = () => {
    const file = carBackRef.current.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
        setCarBackImg(reader.result);
    };
    setCarBackState(true);
  };

  const saveCarLeftImg = () => {
    const file = carLeftRef.current.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
        setCarLeftImg(reader.result);
    };
    setCarLeftState(true);
  };

  const saveCarRightImg = () => {
    const file = carRightRef.current.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
        setCarRightImg(reader.result);
    };
    setCarRightState(true);
  };

  const onResultClick = () => {
    setUploadingImg("");
    console.log("사진 전송이 click!!!!");
    alert("전송되었습니다!");
  }

  const onFeedbackClick = () => {
    console.log("click!!!!");
    alert("전송되었습니다!");
  }

  return (
    <div className="page">
      {/* -----고객/차량 정보----- */}
      <div className="userInfo">
        <h1 align="center">RDCs</h1>
        <form >
          <InputWithLabel
            value={userName}
            type="Text"
            label="이름"
            placeholder="이름을 입력해주세요"
            disabled={disabledUserinfo}
            onChange={onChangeuserName}/>
          <InputWithLabel
            value={carNum}
            type="Text"
            label="차량번호"
            placeholder="차량번호를 입력해주세요"
            disabled={disabledUserinfo}
            onChange={onChangecarNum}/>
          <InputWithLabel
            value={userPhone}
            type="Tel"
            label="전화번호"
            placeholder="전화번호를 입력해주세요"
            disabled={disabledUserinfo}
            onChange={onChangeuserPhone}/>
          <SelectWithLabel
            value={userRent}
            type="Text"
            label="대여/반납"
            disabled={disabledUserinfo}
            onChange={onChangeuserRent}>
            <option value="대여">대여</option>
            <option value="반납">반납</option>
          </SelectWithLabel>

        <div align="center">
          <button className="submitButton" 
            disabled={allowUserinfo}
            onClick={onSubmitClick}
          >조회하기
          </button>
        </div>
        </form>
      </div>

      {/* -----차량 이미지 업로드----- */}
      <div className="uploadCarImage" align="center" style={{display: loadingUserinfo}}>
        <div style={{float:"left", marginRight:"10px"}}>
          <img className="carImage" src={carFrontImg ? carFrontImg : carFrontPrev} alt="차량 전면 이미지" />
          <form>
            <label className="carImgLabel"  htmlFor="carFront">{carFrontImg ? "차량 전면 이미지 추가 완료" : "차량 전면 이미지를 추가해주세요"}</label>
            <input className="carImgInput" type="file" accept="image/*" id="carFront" onChange={saveCarFrontImg} ref={carFrontRef}/>
          </form>
        </div>

        <div style={{float:"right"}}>
          <img className="carImage" src={carBackImg ? carBackImg : carBackPrev} alt="차량 후면 이미지"/>
            <form>
              <label className="carImgLabel"  htmlFor="carBack">{carBackImg ? "차량 후면 이미지 추가 완료" : "차량 후면 이미지를 추가해주세요"}</label>
              <input className="carImgInput" type="file" accept="image/*" id="carBack" onChange={saveCarBackImg} ref={carBackRef} />
            </form>
        </div>

        <div style={{float:"left", marginRight:"10px"}}>
            <img className="carImage" src={carLeftImg ? carLeftImg : carLeftPrev} alt="차량 좌측 이미지"/>
            <form>
              <label className="carImgLabel" htmlFor="carLeft">{carLeftImg ? "차량 좌측 이미지 추가 완료" : "차량 좌측 이미지를 추가해주세요"}</label>
              <input className="carImgInput" type="file" accept="image/*" id="carLeft" onChange={saveCarLeftImg} ref={carLeftRef}/>
            </form>
        </div>

        <div style={{float:"right"}}>
            <img className="carImage" src={carRightImg ? carRightImg : carRightPrev} alt="차량 우측 이미지"/>
            <form>
              <label className="carImgLabel" htmlFor="carRight">{carRightImg ? "차량 우측 이미지 추가 완료" : "차량 우측 이미지를 추가해주세요"}</label>
              <input className="carImgInput" type="file" accept="image/*" id="carRight" onChange={saveCarRightImg} ref={carRightRef}/>
            </form>
        </div>
        
        <br></br>
        <div align="center">
          <button className="submitButton"
            onClick={onResultClick}
            disabled={(carFrontState && carBackState && carLeftState && carRightState) ? false : true}>
            {(carFrontState && carBackState && carLeftState && carRightState) ? "사진 전송하기" : "사진 업로드 중"}
          </button>
        </div>
      </div>

      {/* -----결과 리턴----- */}
      <div align="center" style={{display: uploadingImg}}>
        <div style={{float:"left", marginRight: "10px"}}>
          <img className="carImage" src={carFrontPrev} alt="차량 전면 이미지 결과"></img>
          <form>
            <label className="carImgLabel" htmlFor="carFrontRes">{"차량 전면 이미지 결과"}</label>
          </form>
        </div>
        <div style={{float:"right"}}>
          <img className="carImage" src={carBackPrev} alt="차량 후면 이미지 결과"></img>
          <form>
            <label className="carImgLabel" htmlFor="carBackRes">{"차량 후면 이미지 결과"}</label>
          </form>
        </div>
        <div style={{float:"left", marginRight: "10px"}}>
          <img className="carImage" src={carLeftPrev} alt="차량 죄측 이미지 결과"></img>
          <form>
            <label className="carImgLabel" htmlFor="carLeftRes">{"차량 좌측 이미지 결과"}</label>
          </form>
        </div>
        <div style={{float:"right"}}>
          <img className="carImage" src={carRightPrev} alt="차량 우측 이미지 결과"></img>
          <form>
            <label className="carImgLabel" htmlFor="carRightRes">{"차량 우측 이미지 결과"}</label>
          </form>
        </div>

        <div align="center">
          <button className="submitButton" onClick={onFeedbackClick} disabled={false}>피드백 전송</button>
        </div>
      </div>  

    </div>
  );
  
}

export default App;