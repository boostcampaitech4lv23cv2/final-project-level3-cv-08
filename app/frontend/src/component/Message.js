import React from 'react'

function Message(props){
    return(
        <h1 disabled={props.disabled}>Message!</h1>
    );
}

export default Message;