import React from 'react';
import styled from 'styled-components';
import oc from 'open-color';

// 두개가 함께 있을땐 상단 (그 사이) 에 여백을 준다
const Wrapper = styled.div`
    & + & {
        margin-top: 1rem;
    }
`;

const Label = styled.div`
    font-size: 1rem;
    font-family: 'NanumBarunGothic';
    color: ${oc.gray[6]};
    margin-bottom: 0.25rem;
    margin-top: 1rem;
`;

const Select = styled.select`
    font-family: 'NanumBarunGothic';
    width: 98%;
    height: 2.5rem;
    border: 1px solid ${oc.gray[3]};
    outline: none;
    border-radius: 10px;
    line-height: 2.5rem;
    font-size: 1.2rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem; 
`;

// rest 쪽에는 onChange, type, name, value, placeholder 등의 input 에서 사용 하는 값들을 넣어줄수 있다.
const SelectWithLabel = ({label, ...rest}) => (
    <Wrapper>
        <div className="wrapperLabel">
            <Label>{label}</Label>
        </div>
        <div className="wrapperInput">
            <Select {...rest}/>
        </div>
    </Wrapper>
);

export default SelectWithLabel;