// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

contract SimpleStorage {
    //initialized to 0
    uint256 magicNumber;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        magicNumber = _favoriteNumber;
    }

    //view and pure require no transaction
    function retrieve() public view returns (uint256) {
        return magicNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
