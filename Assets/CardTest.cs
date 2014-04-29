using UnityEngine;
using System.Collections;

public class CardTest : MonoBehaviour {

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
        if (Input.GetMouseButtonDown(0)) {
            GetComponent<CardController>().number = Random.Range(1, 13);
            GetComponent<CardController>().suit = Random.Range(1, 4);
        }
	}
}
