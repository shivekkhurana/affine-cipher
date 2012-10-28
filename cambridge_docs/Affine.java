/*************************************************************************/
/*PRIYA RAMAKRISHNAN                                                     */
/*                                                                       */
/*Affine Cipher Decryption Tool                                          */
/*CMSC 443                                                               */
/*-----------------------------------------------------------------------*/
/*To compile into Java byte code:                                        */
/*    javac Affine.java                                                  */
/*To run the program                                                     */
/*    java Affine                                                        */
/*Minimal operating instructions:                                        */ 
/*      1. load in cipher text                                           */
/*      2. hit decrypt                                                   */
/*      3. if this is the correct plaintext, save plaintext & key.       */
/*      4. otherwise, hit try again.                                     */
/*      5. save plaintext                                                */
/*-----------------------------------------------------------------------*/
/*This project attempts to automate the breaking of a simple affine      */
/*substitution cipher. It does this by first determining the most        */
/*frequently occuring ciphertext characters. It then maps 'e' to the     */
/*most frequently occuring character and 't' to the next. If this creates*/
/*a valid key (a is relatively prime), then it decrypts the rest of the  */
/*plainText and shows the key and the plainText to the user.             */
/*                                                                       */
/*If this is not a valid key or if the user wants to try again, it keeps */
/*e mapped to the most frequently occuring character and maps t to the   */
/*third most frequently occuring character. It continues to do this until*/
/*T has been mapped to "ROUNDS" number of characters. (ROUNDS=7: Can be  */  
/*changed if needed). At this time, e is mapped to the second most       */
/*frequently occuring char and 't' to the most. This loop of mapping e   */
/*and t continues until both 'e' and 't' have been mapped to all of the  */
/*combinations of "ROUNDS" characters.                                   */ 
/*-----------------------------------------------------------------------*/
/*Limitations: Assumes that in the plaintext, the letters 'e' and 't'    */
/*are one of the "ROUNDS" most frequently occuring characters. This can  */
/*be changed by changing "ROUNDS" to 26. However, this does not solve the*/
/*case when 'e' and 't' do not occur at all in the plainText. Also,      */
/*assumes that the plainText is enciphered in modulo 26.                 */  
/*************************************************************************/


import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.*;


public class Affine extends Frame implements WindowListener
{
  
  /*Screen Components*/
  MenuBar menuBar;
  Menu fileMenu;
  MenuItem savePT;
  MenuItem openCT;
  MenuItem saveKey;
  MenuItem quit;
  
  Button decrypt;
  
  TextArea plainText;	
  TextArea cipherText;
  TextArea keyText;
  
  /*Number of letters that 'e' and 't' map to*/
  final int ROUNDS = 7;

  /*System of equations: mapping of 'e' and 't'*/
  final int[][] etMatrix = {{4,19},{1,1}}; 

  /*Inverse of the above Matrix*/
  final int[][] etMatrixInverse = {{19,3},{7,24}};

  /*Array of Numbers that are Relatively Prime to 26*/
  final int[] relativelyPrimeTo26 = {1,3,5,7,9,11,15,17,19,21,23,25};
  
  /*Initialize*/
  int E_Index=0;
  int T_Index=1;
  
  /*Array consisting of most frequently occuring characters. Total: ROUNDS.*/
  int freqCharIdx[];
  
  /*Suggested Mapping of 'e' and 't'*/
  int guessMatrix[];

  /*Values for a and b*/
  int abMatrix[];
  
  /*Handels Window Events*/
  public void windowActivated(WindowEvent e) {;}
  public void windowClosed(WindowEvent e) {;}
  public void windowDeactivated(WindowEvent e) {;}
  public void windowDeiconified(WindowEvent e) {;}
  public void windowIconified(WindowEvent e) {;}
  public void windowOpened(WindowEvent e) {;}
  /*Destroy Window and Exit*/
  public void windowClosing(WindowEvent e){
    setVisible(false);
    dispose();
    System.exit(0);
  }



  /*****************************************************************/
  /*Affine(): Initializes frame with Title, Foreground & Background*/
  /*Color.                                                         */
  /*****************************************************************/  
    
  public Affine()
    {
      super("Affine Cipher Decryption Tool");
      this.setBackground(java.awt.Color.white);
      this.setForeground(new java.awt.Color(0, 0, 100));
      
      this.addWindowListener(this);
    }

  
  /*****************************************************************/
  /*main(): Creates a new Affine object and start it up.           */
  /*****************************************************************/  

  public static void main(String args[])
    {
      Affine a = new Affine();
      a.startup();
    }
  

  /*****************************************************************/
  /*startup(): Sets up the window and handles the events of all    */
  /*window components.                                             */
  /*****************************************************************/  

  public void startup()
    {
      
      setupMenuBar();
      
      /*Cipher Text Area and it's attributes*/
      cipherText = new TextArea(8,30);
      cipherText.setEditable(false);
      cipherText.setBounds(7,97,619,109);
      
      /*Plain Text Area and it's attributes*/
      plainText = new TextArea(8,30);
      plainText.setEditable(false);
      plainText.setBounds(7,250,619,109);
      
      /*Key Text Area and it's attributes*/
      keyText = new TextArea(8,30);
      keyText.setEditable(false);
      keyText.setBounds(7,403,619,90);
      
      /*Decrypt Button and it's attributes*/
      decrypt = new Button("Decrypt");
      decrypt.setEnabled(false);
      decrypt.setBounds(11,510,125,30);
      
      /*Title of the Window*/
      Label titleLabel = new Label("Affine Cipher Decryption Tool", Label.CENTER);
      titleLabel.setFont(new java.awt.Font("Serif", 1, 16));
      titleLabel.setBounds(143, 50, 356, 34);
      
      /*My Name*/
      Label nameLabel = new Label();
      nameLabel.setFont(new java.awt.Font("Serif", 3, 14));
      nameLabel.setText("-Priya Ramakrishnan");
      nameLabel.setBounds(480, 512, 145, 35);
      
      /*Cipher Text Label*/
      Label CTLabel = new Label();
      CTLabel.setFont(new java.awt.Font("Serif", 3, 14));
      CTLabel.setText("Cipher Text:");
      CTLabel.setBounds(9, 68, 125, 30);
      
      /*Plain Text Label*/
      Label PTLabel = new Label();
      PTLabel.setFont(new java.awt.Font("Serif", 3, 14));
      PTLabel.setText("Plain Text:");
      PTLabel.setBounds(9, 224, 125, 30);
      
      /*Key Text Label*/
      Label KeyLabel = new Label();
      KeyLabel.setFont(new java.awt.Font("Serif", 3, 14));
      KeyLabel.setText("Key Text:");
      KeyLabel.setBounds(9, 380, 125, 20);
      
      /*Layout and size of Window*/
      this.setLayout(null);
      this.setSize(631,560);
      
      /*Add all components to Window*/
      this.add(plainText);
      this.add(cipherText);
      this.add(keyText);
      this.add(decrypt);
      this.add(titleLabel);
      this.add(nameLabel);
      this.add(PTLabel);
      this.add(CTLabel);
      this.add(KeyLabel);
      
      /*Pack it up and make it visible*/
      this.pack();
      this.setVisible(true);
      
      /*Handle the event when user chooses to open Cipher Text*/
      openCT.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e){
	  
	  /*Read the ciphertext from file and put it in the*/
	  /*Cipher TextArea and pack the window*/
	  LoadCT();
	  pack();
	  
	  decrypt.setLabel("Decrypt");
	  savePT.setEnabled(false);
	  saveKey.setEnabled(false);
	  
	  /*If there is ciphertext, enable the decrypt button*/
	  if(cipherText.getText().length() !=0)
	    decrypt.setEnabled(true);
	  else decrypt.setEnabled(false);	
	  
	}			
      });	
      
      /*Handle the event when user chooses to save Plain Text*/
      savePT.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e){
	  
	  saveText(plainText);
	}			
      });
      
      /*Handle the event when user chooses to save Key Text*/
      saveKey.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e){
	  
	  saveText(keyText);
	}			
      });
      
      /*If user decides to quit, close window and exit*/
      quit.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e){
	  
	  setVisible(false);
	  dispose();
	  System.exit(0);
	}
      });	
      
      /*Handle event when user clicks on decrypt button*/
      decrypt.addActionListener(new ActionListener() {
	public void actionPerformed(ActionEvent e){
	  
	  int a;
	  /*clear the Plain Text and Key Text*/
	  plainText.setText("");
	  keyText.setText("");
	  
	  /*Get Frequency counts of Cipher Text*/
	  getFrequency();

	  /*Map 'e' and 't' to ciphertext characters and*/
	  /*solve for a and b (abMatrix)                */
	  get_abMatrix();
	  
	  /*Check to see if a is relatively prime to 26.*/
	  /*If not, map 'e' and 't' to another pair of  */
	  /*ciphertext characters and generate another  */
	  /*abMatrix. Continue to do so until all ROUNDS*/
	  /*are finished or a is relatively prime to 26.*/
	  a=abMatrix[0];
	  if( (relativelyPrime(a) == false) && 
	      (E_Index != ROUNDS-1) && 
	      (T_Index != ROUNDS-1) ){
	    while(relativelyPrime(a) == false){
	      get_abMatrix();
	      a=abMatrix[0];					
	    }
	  }

	  /*Decrypt the Cipher Text and place add the Plain*/
	  /*Text and Key in the relative text areas.       */
	  decryptCipher();
	  
	  /*Enable the save menu items*/
	  savePT.setEnabled(true);
	  saveKey.setEnabled(true);

	  /*Pack the Window*/
	  pack();
	}
      });	
    }

  
  /*****************************************************************/
  /*decryptCipher(): Since d(y) = (inverse a)(y-b) and we know both*/
  /*a and b through the already calculated abMatrix, we can find   */
  /*d(y) for each character y in the ciphertext to generate the    */
  /*plaintext.                                                     */
  /*****************************************************************/ 
  
  public void decryptCipher()
    {
      /*Read in Cipher Text from Text Area*/
      String ciphertext = new String(cipherText.getText());
      
      /*Determine inverse(a) and b*/
      int invA = modInverse(abMatrix[0]);
      int b = abMatrix[1];

      /*for each ciphertext character c, if c is a letter, find d(c)*/
      /*and append it to the plainText. If c is not a letter, append*/
      /*the character to the plainText.                             */
      for(int i=0; i<ciphertext.length();i++){
	char c = ciphertext.charAt(i);
	if(java.lang.Character.isLetter(c))
	  {
	    int y = MapAlphabet(c);
	    int x= (invA*(y-b))%26;
	    if(x<0) {x=26+x;}
	   
	    Character ptchar = new Character(MapNumber(x));
	    plainText.append(ptchar.toString());
	  }
	else{
	  Character ptchar = new Character(c);
	  plainText.append(ptchar.toString());
	}
      }
      
      /*Append the key to the Key Text Area*/
      Integer ia = new Integer(invA);
      Integer b1 = new Integer(b);
      keyText.append("d(y) = "+ ia.toString()
		     +"(y-" + b1.toString()+ ") mod 26");
    }
  

  /*****************************************************************/
  /*modInverse(): Takes in an integer that is relatively prime to  */
  /*26 and returns the inverse of it. If the number is not rel.    */
  /*prime to 26 (An error), returns 100.                           */
  /*****************************************************************/ 

  public int modInverse(int a)
    {
      if(a==1) return 1; if(a==3) return 9;
      if(a==5) return 21; if(a==7) return 15;
      if(a==9) return 3; if(a==11) return 19; 
      if(a==15) return 7;if(a==17) return 23;
      if(a==19) return 11; if(a==21) return 5;
      if(a==23) return 17; if(a==25) return 25;
      
      return 100;
    }
	
  
  /*****************************************************************/
  /*setupMenuBar(): Creates menu components and assigns attributes */
  /*and places them on the window.                                 */
  /*****************************************************************/ 

  public void setupMenuBar()
    {
      menuBar = new MenuBar();
      fileMenu = new Menu("File");
      openCT = new MenuItem("Open Cipher Text");
      savePT = new MenuItem("Save Plain Text");		
      saveKey = new MenuItem("Save Key");
      quit = new MenuItem("Quit");
      
      savePT.setEnabled(false);
      saveKey.setEnabled(false);

      fileMenu.add(openCT);
      fileMenu.add(savePT);
      fileMenu.add(saveKey);
      fileMenu.add(quit);
      menuBar.add(fileMenu);		
      this.setMenuBar(menuBar);	
    }
  

  /*****************************************************************/
  /*relativelyPrime(): Takes in an integer and returns a boolean   */
  /*indicating whether the number is relatively prime to 26. Uses  */
  /*the relativelyPrimeTo26 array.                                 */
  /*****************************************************************/ 
  
  public boolean relativelyPrime(int a)
    {
      for(int i=0; i<12; i++){
	if(a==relativelyPrimeTo26[i]) return true;
      }
      return false;
    }
  

  /*****************************************************************/
  /*get_abMatrix(): Maps 'e' and 't' to characters in CipherText.  */
  /*This results in the guess Matrix. We now have a system of      */
  /*equations: {{4,19},{1,1}}*{a,b} = guessMatrix. To determine    */
  /*the abMatrix, we multiply the inverse of the etMatrix and the  */
  /*guessMatrix.                                                   */
  /*****************************************************************/ 
  public void get_abMatrix()
    {
      guessMatrix = new int[2];
      
      guessMatrix[0] = freqCharIdx[E_Index];
      guessMatrix[1] = freqCharIdx[T_Index];
      
      incrementIndexes();
      abMatrix = matrixMultiplyMod26(etMatrixInverse, guessMatrix);			
      
    }
  

  /*****************************************************************/
  /*matrixMultiplyMod26(): Takes in a 2x2 Matrix and a 1x2 Matrix  */
  /*and returns their product mod 26: a 1x2 Matrix.                */ 
  /*****************************************************************/ 

  int[] matrixMultiplyMod26(int a[][], int b[])
    {
      int ans;
      int c[] = new int[2];
      
      c[0] = ((a[0][0] * b[0]) + (a[1][0] * b[1]))%26;
      c[1] = ((a[0][1] * b[0]) + (a[1][1] * b[1]))%26;
      return c;
    }
  

  /*****************************************************************/
  /*incrementIndexes(): Used to map 'e' and 't' to characters in   */
  /*Cipher Text. The freqCharIdx[] consists of 'ROUNDS' number of  */
  /*the most frequently occuring characters. E_INDEX is the index  */
  /*of the character in freqCharIdx that 'e' maps to. T_INDEX is   */
  /*is the character in freqCharIdx that 't' maps to. This function*/
  /*increments T_INDEX and E_INDEX and if all ROUNDS are finished  */
  /*sends a notice that it couldn't find any more solutions.       */
  /*****************************************************************/ 
  
  public void incrementIndexes()
    {
      /*No more mappings available. Start Finished Panel*/
     if((E_Index == ROUNDS-1) && (T_Index == ROUNDS-2)){
	decrypt.setLabel("No More");
	decrypt.setEnabled(false);
	setupFinishedPanel();
      }	
     
     /*All mappings of T with current mapping of E is   */
     /*finished. Map 'e' to the next frequently occuring*/
     /*character by incrementing E_Index and set T_Index*/
     /*to 0.                                            */
      else if(T_Index == ROUNDS-1){
	E_Index++;
	T_Index=0;
	decrypt.setLabel("Try Again");
      }
     
     /*Otherwise, increment T_Index. If T_Index and*/
     /*E_Index are equal, they are mapping to the  */
     /*same letter, so increment T_Index again.    */
      
      else{
	T_Index++;
	if(T_Index==E_Index) T_Index++;
	decrypt.setLabel("Try Again");		
      }
    }
 

  /*****************************************************************/
  /*setupFinishedPanel(): Setup the Panel that is displayed when   */
  /*there are no more solutions.                                   */
  /*****************************************************************/

 public void setupFinishedPanel()
   {
     Label errorLabel = new Label("Sorry, No More Solutions",Label.CENTER);
     Button errorButton = new Button("OK");
     
     this.removeAll();
     this.setMenuBar(null);
     
     errorButton.setBounds(35, 91, 125, 30);
     errorLabel.setFont(new java.awt.Font("Serif", 1, 14));
     errorLabel.setBounds(25, 51, 150, 34);
     
    
     this.add(errorButton);
     this.add(errorLabel);	
     
     this.setLayout(null);
     this.setSize(200,150);
     this.pack();
     this.setVisible(true);
     
     /*When user clicks "OK" button, close window and exit*/
     errorButton.addActionListener(new ActionListener() {
       public void actionPerformed(ActionEvent e){
	 setVisible(false);
	 dispose();
	 System.exit(0);
	 
       }
     });	
     
   }	
  
  /*****************************************************************/
  /*getFrequency(): determines the most frequently occuring chars  */
  /*in ciphertext and places the "ROUNDS" most frequently occuring */
  /*ones in freqCharIdx[] (Index 0 is the most frequently occuring */
  /*character,                                                     */
  /*****************************************************************/
 
 public void getFrequency()
    {
      String ciphertext = cipherText.getText();
      int charfreq[] = new int[26];
      freqCharIdx = new int[ROUNDS];
      int idx=0;
      
      /*Determine the number of times each character appears in CT: */
      /*For each ciphertext character c, if c is a letter, determine*/
      /*the number c maps to (A->1) and increment that position in  */
      /*charfreq[].                                                 */

      for(int i=0; i<ciphertext.length(); i++){
	
	if(java.lang.Character.isLetter(ciphertext.charAt(i))){
	  idx = MapAlphabet(ciphertext.charAt(i));
	  charfreq[idx]++;
	}
      }
      
      /*Place the "ROUNDS" most frequently occuring ones in*/
      /*freqCharIdx.                                       */

      for(int i=0; i<ROUNDS; i++){
	int max=0;
	for(int j=0; j<26; j++){
	  if(charfreq[j] > max){
	    max = charfreq[j];
	    idx=j;
	  }
	}
	freqCharIdx[i]=idx;
	charfreq[idx]=-1;
      }			
      
    }

  /*****************************************************************/
  /*saveText(): Bring up a File Dialog Box and save text in given  */
  /*TextArea to file.                                              */
  /*****************************************************************/
  
  public void saveText(TextArea T)
    {
      try{
	FileDialog fd = new FileDialog(this, "Save", FileDialog.SAVE);
	fd.setVisible(true);
	String s = fd.getFile();
	if(s!=null){
	  File outf = new File(s);
	  PrintWriter out = new PrintWriter(new FileOutputStream(outf));
	  String st = T.getText();
	  out.print(st);
	  out.flush();
	  out.close();
	}
      }
      
      catch (IOException se) {System.err.println("Caught" + se);}
    }		
  

  /*****************************************************************/
  /*LoadCT(): Bring up File Dialog box and load ciphertext into the*/
  /*text area. Clear the plain Text Area and the key Text Area.    */
  /*****************************************************************/

  public void LoadCT()
    {
      File inf;
      
      try {		
	FileDialog fd = new FileDialog(this,"Open",FileDialog.LOAD);
	fd.setVisible(true);
	String s = fd.getFile();
	if(s!=null){
	  plainText.setText("");
	  cipherText.setText("");
	  T_Index = E_Index = 0;
	  keyText.setText("");
	  inf = new File(s);
	  BufferedReader in = new BufferedReader(new FileReader(inf));
	  String l = new String();
	  while ((l=in.readLine()) != null){
	    cipherText.append(l.toLowerCase() + "\n");
	  }
	} 		
	
      }
      catch (IOException b) {System.err.println("Caught: "+b);}
    }		 	
  
  /*****************************************************************/
  /*MapAlphabet: Takes in an alphabetic character and returns the  */
  /*Integer index of it.                                           */
  /*****************************************************************/
  public int MapAlphabet(char c)
    {
      if (c=='a') return 0; if(c=='b') return 1; if(c=='c') return 2;
      if (c=='d') return 3; if (c=='e') return 4; if (c=='f') return 5;
      if (c=='g') return 6; if (c=='h') return 7; if (c=='i') return 8;
      if (c=='j') return 9; if (c=='k') return 10; if (c=='l') return 11;
      if (c=='m') return 12; if (c=='n') return 13; if (c=='o') return 14;
      if (c=='p') return 15; if (c=='q') return 16; if (c=='r') return 17;
      if (c=='s') return 18; if (c=='t') return 19; if (c=='u') return 20;
      if (c=='v') return 21; if (c=='w') return 22; if (c=='x') return 23;
      if (c=='y') return 24; if (c=='z') return 25;
      return 100;
    }		
  
  
  /*****************************************************************/
  /*MapNumber(): Takes in an integer and returns the character that*/
  /*the integer maps to.                                           */
  /*****************************************************************/
  
  public char MapNumber(int i)
    {
      if (i==0) return 'a'; if(i==1) return 'b'; if(i==2) return 'c';
      if (i==3) return 'd'; if (i==4) return 'e'; if (i==5) return 'f';
      if (i==6) return 'g'; if (i==7) return 'h'; if (i==8) return 'i';
      if (i==9) return 'j'; if (i==10) return 'k'; if (i==11) return 'l';
      if (i==12) return 'm'; if (i==13) return 'n'; if (i==14) return 'o';
      if (i==15) return 'p'; if (i==16) return 'q'; if (i==17) return 'r';
      if (i==18) return 's'; if (i==19) return 't'; if (i==20) return 'u';
      if (i==21) return 'v'; if (i==22) return 'w'; if (i==23) return 'x';
      if (i==24) return 'y'; if (i==25) return 'z';
      return '%';
    }	
  
  
}		



		



