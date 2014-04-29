using UnityEngine;
using UnityEditor;
using System.Collections;
using System.Linq;

public class CardController : MonoBehaviour {
    public int suit;
    public int number;
    public string card;

    private Sprite[] suits;
    private Sprite[] numbers;

    private SpriteRenderer suitRenderer;
    private SpriteRenderer numberRenderer;
    private SpriteRenderer cardRenderer;

    Sprite[] loadSprites(string path)
    {
        return AssetDatabase.LoadAllAssetRepresentationsAtPath(path)
            .OfType<Sprite>().ToArray();
    }

    // Use this for initialization
    void Start () {
        suits = loadSprites("Assets/Cards/suit.png");
        numbers = loadSprites("Assets/Cards/cardnum.png");


        var sprits = GetComponentsInChildren<SpriteRenderer>();
        numberRenderer = sprits.Where(s => s.name == "number").Single();
        suitRenderer = sprits.Where(s => s.name == "suit").Single();
        cardRenderer = sprits.Where(s => s.name == "card").Single();
    }
    
    // Update is called once per frame
    void Update () {
        if (suit != 0) {
            suitRenderer.enabled = true;
            suitRenderer.sprite = suits[suit - 1];
        } else {
            suitRenderer.enabled = false;
        }
        if (number != 0) {
            numberRenderer.enabled = true;
            numberRenderer.sprite = numbers[(1 - suit % 2) * 13 + number - 1];
        } else {
            numberRenderer.enabled = false;
        }
    }
}