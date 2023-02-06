import React from 'react';
import { useState, useEffect, useRef } from 'react';
import carFrontPrev from '../images/carFront.png'
import carBackPrev from '../images/carBack.png'
import carLeftPrev from '../images/carLeft.png'
import carRightPrev from '../images/carRight.png'

function UploadImage(uploaded){
    const [carFrontImg, setCarFrontImg] = useState("");
    const [carBackImg, setCarBackImg] = useState("");
    const [carLeftImg, setCarLeftImg] = useState("");
    const [carRightImg, setCarRightImg] = useState("");

    const [carFrontState, setCarFrontState] = useState(false);
    const [carBackState, setCarBackState] = useState(false);
    const [carLeftState, setCarLeftState] = useState(false);
    const [carRightState, setCarRightState] = useState(false);

    const [uploadImg, setUploadImg] = useState(false);

    const carFrontRef = useRef();
    const carBackRef = useRef();
    const carLeftRef = useRef();
    const carRightRef = useRef();

    // 이미지 업로드 input의 onChange
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

    const onSubmitClick = () => {
        console.log("click!!!!");
        alert("전송되었습니다!");
    }

    return(
        <div align="center">
            <div style={{float:"left", marginRight:"10px"}}>
                <img
                    src={carFrontImg ? carFrontImg : carFrontPrev}
                    alt="이미지"
                    width="200"
                    height="150"
                />
                <form>
                    <label 
                        className="carImgLabel" 
                        htmlFor="carFront"
                        >{carFrontImg ? "차량 전면 이미지 추가 완료" : "차량 전면 이미지를 추가해주세요"}
                    </label>
                    <input
                        className="carImgInput"
                        type="file"
                        accept="image/*"
                        id="carFront"
                        onChange={saveCarFrontImg}
                        ref={carFrontRef}
                    />
                </form>
            </div>

            <div style={{float:"right"}}>
                <img
                    src={carBackImg ? carBackImg : carBackPrev}
                    alt="이미지"
                    width="200"
                    height="150"
                />
                <form>
                    <label 
                        className="carImgLabel" 
                        htmlFor="carBack"
                        >{carBackImg ? "차량 후면 이미지 추가 완료" : "차량 후면 이미지를 추가해주세요"}
                    </label>
                    <input
                        className="carImgInput"
                        type="file"
                        accept="image/*"
                        id="carBack"
                        onChange={saveCarBackImg}
                        ref={carBackRef}
                    />
                </form>
            </div>

            <div style={{float:"left", marginRight:"10px"}}>
                <img
                    src={carLeftImg ? carLeftImg : carLeftPrev}
                    alt="이미지"
                    width="200"
                    height="150"
                />
                <form>
                    <label 
                        className="carImgLabel" 
                        htmlFor="carLeft"
                        >{carLeftImg ? "차량 좌측 이미지 추가 완료" : "차량 좌측 이미지를 추가해주세요"}
                    </label>
                    <input
                        className="carImgInput"
                        type="file"
                        accept="image/*"
                        id="carLeft"
                        onChange={saveCarLeftImg}
                        ref={carLeftRef}
                    />
                </form>
            </div>

            <div style={{float:"right"}}>
                <img
                    src={carRightImg ? carRightImg : carRightPrev}
                    alt="이미지"
                    width="200"
                    height="150"
                />
                <form>
                    <label 
                        className="carImgLabel" 
                        htmlFor="carRight"
                        >{carRightImg ? "차량 우측 이미지 추가 완료" : "차량 우측 이미지를 추가해주세요"}
                    </label>
                    <input
                        className="carImgInput"
                        type="file"
                        accept="image/*"
                        id="carRight"
                        onChange={saveCarRightImg}
                        ref={carRightRef}
                    />
                </form>
            </div>
            
            <br></br>
            <div align="center">
                <button className="submitButton"
                    onClick={onSubmitClick}
                    disabled={(carFrontState && carBackState && carLeftState && carRightState) ? false : true}
                    style={{backgroundColor: (carFrontState && carBackState && carLeftState && carRightState) ? "#0095f6" : "#C3C3C3",
                        borderRadius: 10,
                        padding: "10px 20px",
                        border: 0,
                        color: "white",
                        fontSize: "1.2rem",
                        fontFamily: "NanumBarunGothic",
                        display: "inline-block",}}>
                    {(carFrontState && carBackState && carLeftState && carRightState) ? "사진 전송하기" : "사진 업로드 중"}
                </button>
            </div>

        </div> 
    );
}

export default UploadImage;