import React from 'react';
import { useState, useEffect, useRef } from 'react';
import InputWithLabel from './InputWithLabel';
import SelectWithLabel from './SelectWithLabel';

function Userinfo(){
    const [userName, setuserName] = useState("");
    const [carNum, setcarNum] = useState();
    const [userPhone, setuserPhone] = useState();
    const [userRent, setuserRent] = useState();
    const [loadingUserinfo, setLoadingUserinfo] =useState(false);

    const onChangeuserName = (event) => setuserName(event.target.value);
    const onChangecarNum = (event) => setcarNum(event.target.value);
    const onChangeuserPhone = (event) => setuserPhone(event.target.value);
    const onChangeuserRent = (event) => setuserRent(event.target.value);

    const onSubmit = (event) => {
        event.preventDefault();
        if (userName === "" | carNum === "" | userPhone === ""){
            return;
        }
        else {
            console.log("submit");
            setLoadingUserinfo(true);
        }
    };
    return(
        <div>
            <h1 align="center">RDCs</h1>
            <form onSubmit={onSubmit}>
                <InputWithLabel
                    value={userName}
                    type="Text"
                    label="이름"
                    placeholder="이름을 입력해주세요"
                    onChange={onChangeuserName}/>
                <InputWithLabel
                    value={carNum}
                    type="Text"
                    label="차량번호"
                    placeholder="차량번호를 입력해주세요"
                    onChange={onChangecarNum}/>
                <InputWithLabel
                    value={userPhone}
                    type="Tel"
                    label="전화번호"
                    placeholder="전화번호를 입력해주세요"
                    onChange={onChangeuserPhone}/>
                <SelectWithLabel
                    value={userRent}
                    type="Text"
                    label="대여/반납"
                    onChange={onChangeuserRent}>
                    <option value="대여">대여</option>
                    <option value="반납">반납</option>
                </SelectWithLabel>
                <br></br>
            </form>
        </div> 
    );
}

export default Userinfo;