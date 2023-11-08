export default function useFetch(base){
    function get(url) {
        let endpointUlr = base + url;
        return fetch(endpointUlr)
            .then(resp => resp.json())
            .catch(err => console.log(err))
    }

    return {get};
};