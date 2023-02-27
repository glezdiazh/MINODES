# -*- coding: cp1252 -*-
# min attack = 10%, max = 100%

# main window

import wx, sys, os, random, time, datetime
from wx.lib.buttons import GenBitmapTextButton
from numpy import *
import networkx as nx
import operator

orig_dir=os.getcwd()+"\\" # get the current path to be used for all functions

import MCCN    # MCCN function
import htlmDoc

class MyMenu(wx.Frame):
    def __init__(self, parent, id, title):
        # colourGUI='#FFCC66'
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(380, 560),style=wx.CAPTION | wx.SYSTEM_MENU | wx.MINIMIZE_BOX | wx.CLOSE_BOX)
        self.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        # self.SetBackgroundColour(colourGUI)
        self.statusbar = self.CreateStatusBar()        
        self.statusbar.SetStatusText("Ready for your calculations")
        
        # files inputs
        br1=wx.Button(self, 20, 'Chose File Directory', (10,10))
        self.Net = wx.TextCtrl(self, -1, "",(10,40) , (350,-1) ,  style=wx.TE_LEFT)

        # centrality settings
        wx.StaticBox(self, -1, 'Markov Node Descriptors', (10, 70), size=(350, 285))

        # first column of TIs
        self.nSh=wx.CheckBox(self, -1 ,'Shannon Entropy (MSh)', (20, 90))
        self.nSh.SetValue(True)
        self.nTr=wx.CheckBox(self, -1 ,'Trace/Moment (MTr)', (20, 110))
        self.nTr.SetValue(True)
        self.nH=wx.CheckBox(self, -1 ,'Harary (MH)', (20, 130))
        self.nH.SetValue(True)
        self.nW=wx.CheckBox(self, -1 ,'Wiener (MW)', (20, 150))
        self.nW.SetValue(True)
        self.nS6=wx.CheckBox(self, -1 ,'Gutman (MS6)', (20, 170))
        self.nS6.SetValue(True)
        self.nS=wx.CheckBox(self, -1 ,'Schultz (MS)', (20, 190))
        self.nS.SetValue(True)
        self.nATS=wx.CheckBox(self, -1 ,'Moreau-Broto (MATS)', (20, 210))
        self.nATS.SetValue(True)
        self.nJ=wx.CheckBox(self, -1 ,'Balaban (MJ)', (20, 230))
        self.nJ.SetValue(True)
        self.nX1=wx.CheckBox(self, -1 ,'Randic (MX1)', (20, 250))
        self.nX1.SetValue(True)
        self.nX=wx.CheckBox(self, -1 ,'Kier-Hall (MX)', (20, 270))
        self.nX.SetValue(True)
        self.nG=wx.CheckBox(self, -1 ,'Galves-like (MG)', (20, 290))
        self.nG.SetValue(True)
        self.nL=wx.CheckBox(self, -1 ,'Leverage (ML)', (20, 310))
        self.nL.SetValue(True)
        self.nRu=wx.CheckBox(self, -1 ,'Rucker (MRu)', (20, 330))
        self.nRu.SetValue(True)

        # second column of TIs
        self.nD=wx.CheckBox(self, -1 ,'Degree(MD && MinD && MoutD)', (190, 90)) #for degree
        self.nD.SetValue(True)
        self.nE=wx.CheckBox(self, -1 ,'Ecceentricity(ME)', (190, 110)) 
        self.nE.SetValue(True)
        self.nCl=wx.CheckBox(self, -1 ,'Closeness(MCl)', (190, 130)) 
        self.nCl.SetValue(True)
        self.nR=wx.CheckBox(self, -1 ,'Radiality(MR)', (190, 150)) 
        self.nR.SetValue(True)
        self.nCen=wx.CheckBox(self, -1 ,'Centroid(MCen)', (190, 170))
        self.nCen.SetValue(True)
        self.nCFC=wx.CheckBox(self, -1 ,'CF Closeness(MCFC)', (190, 190)) 
        self.nCFC.SetValue(True)
        self.nB=wx.CheckBox(self, -1 ,'Bergaining(MB)', (190, 210))
        self.nB.SetValue(True)
        self.nK=wx.CheckBox(self, -1 ,'Katz(MK)', (190, 230))
        self.nK.SetValue(True)
        self.nCFB=wx.CheckBox(self, -1 ,'CF Betweeness(MCFB)', (190, 250))
        self.nCFB.SetValue(True)
        self.nMMQ=wx.CheckBox(self, -1 ,'Marrero Quadratic(MMQ)', (190, 270))
        self.nMMQ.SetValue(True)
        self.nMML=wx.CheckBox(self, -1 ,'Marrero Linear(MML)', (190, 290))
        self.nMML.SetValue(True)
        self.nMMmL=wx.CheckBox(self, -1 ,'Marrero Multi-Linear(MMmL)', (190, 310))
        self.nMMmL.SetValue(True)
        self.nAIS=wx.CheckBox(self, -1 ,'Avnir Symetry(MAIS && MARS)', (190, 330))
        self.nAIS.SetValue(True)
        
        wx.StaticText(self, -1, 'Power', (20, 380))
        self.power=wx.SpinCtrl(self, -1, '5', (60, 375), (50, -1), min=1, max=5)

        self.nPairOut=wx.CheckBox(self, -1 ,'Node pair output for statistica', (20, 400))
        self.nPairOut.SetValue(False)

        wx.StaticText(self, -1, ' Until ', (20, 430))
        self.NegPairs=wx.SpinCtrl(self, -1, '1', (60, 425), (50, -1), min=1, max=10)
        wx.StaticText(self, -1, ' time(s) linked pairs for the disconnected pairs', (110, 430))
                
        ## BUTTONS
        self.bSubmit=GenBitmapTextButton(self, 25, wx.Bitmap(orig_dir+'images/gtk-execute.png'), 'Run', (10, 460))
        self.bHelp=GenBitmapTextButton(self, 26, wx.Bitmap(orig_dir+'images/gtk-help.png'), 'Help', (100, 460))
        self.bAbout=GenBitmapTextButton(self, 27, wx.Bitmap(orig_dir+'images/gtk-about.png'), 'About', (190, 460))
        self.bQuit=GenBitmapTextButton(self, 28, wx.Bitmap(orig_dir+'images/gtk-quit.png'), 'Quit', (280, 460))
        self.bSubmit.SetBezelWidth(2)
        self.bHelp.SetBezelWidth(2)
        self.bAbout.SetBezelWidth(2)
        self.bQuit.SetBezelWidth(2)

        wx.EVT_BUTTON(self, 20, self.OnBrowseNet)
        
        wx.EVT_BUTTON(self, 25, self.OnSubmit)
        wx.EVT_BUTTON(self, 26, self.OnHelp)
        wx.EVT_BUTTON(self, 27, self.OnAbout)
        wx.EVT_BUTTON(self, 28, self.OnQuit)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, id=101)
        self.Bind(wx.EVT_MENU, self.OnSubmit, id=100)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=110)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=111)

        # header
        print "\n***************************************************************************"
        print "MI-NODES: MARCH-INSIDE Node Descriptors (ver. 2.0, 2011)\n\nCristian Robert Munteanu (muntisa@gmail.com)\nHumberto Gonzalez-Diaz (gonzalezdiazh@yahoo.es)"
        print "***************************************************************************\n"
        
        self.orig_dir = globals()["orig_dir"] #takes the original folder for the un modified files in the browse control
        self.dirList=[] # list of all the net, mat, dat files in a specific folder; variable for the entire class to be used later
        return
            
    def OnBrowseNet(self,event):
        dialog = wx.DirDialog(None, "Choose a directory:",os.getcwd(), style=wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST|wx.DD_CHANGE_DIR)
        if dialog.ShowModal() == wx.ID_OK:
            self.SetStatusText('You selected: %s\n' %dialog.GetPath())
            self.dirname=dialog.GetPath() # variable with the folder
            self.Net.SetValue(self.dirname)
            for root, dirs, files in os.walk(self.dirname, topdown=False):
                for name in files:
                    sExt=name[len(name)-4:len(name)]
                    if sExt==".net" or sExt==".mat" or sExt==".dat":
                        self.dirList.append(root+"\\"+name) # in the future use root as first/last column!
        dialog.Destroy
        return

    ##################################################################################################################
    # main calculation  (Markov all)
    ##################################################################################################################
    
    def OnSubmit(self, event):
        tt0=time.clock()
        # if no folder is selected, finish the calculation
        if self.Net.GetValue()=="":
            print "-> Please select a directory for the input files and retry!"
            return
        # if the selected folder has no inputs, finish the calculation
        if len(self.dirList)==0:
            print "-> The selected directory do not contains any NET, MAT and DOT file! Please select another directory and retry."
            return
        
        # create dynamic header if TI is selected
        self.listHeader=[] # list with the header centralities
        k=int(self.power.GetValue())

        if self.nSh.GetValue() == True:
            self.listHeader.append("Sh") # for classical non-Markov indices
            for nk in range(k+1): self.listHeader.append("Sh"+str(nk))
        if self.nTr.GetValue() == True:
            self.listHeader.append("Tr")
            for nk in range(k+1): self.listHeader.append("Tr"+str(nk))
        if self.nH.GetValue() == True:
            self.listHeader.append("H")
            for nk in range(k+1): self.listHeader.append("H"+str(nk))
        if self.nW.GetValue() == True:
            self.listHeader.append("W")
            for nk in range(k+1): self.listHeader.append("W"+str(nk))
        if self.nS6.GetValue() == True:
            self.listHeader.append("S6")
            for nk in range(k+1): self.listHeader.append("S6"+str(nk))
        if self.nS.GetValue() == True:
            self.listHeader.append("S")
            for nk in range(k+1): self.listHeader.append("S"+str(nk))
        if self.nATS.GetValue() == True:
            self.listHeader.append("ATS")
            for nk in range(k+1): self.listHeader.append("ATS"+str(nk))
        if self.nJ.GetValue() == True:
            self.listHeader.append("J")
            for nk in range(k+1): self.listHeader.append("J"+str(nk))
        if self.nX1.GetValue() == True:
            self.listHeader.append("X1")
            for nk in range(k+1): self.listHeader.append("X1"+str(nk))
        if self.nX.GetValue() == True:
            self.listHeader.append("X")
            for nk in range(k+1): self.listHeader.append("X"+str(nk))
        if self.nG.GetValue() == True:
            self.listHeader.append("G")
            for nk in range(k+1): self.listHeader.append("G"+str(nk))
        if self.nL.GetValue() == True:
            self.listHeader.append("L")
            for nk in range(k+1): self.listHeader.append("L"+str(nk))
        if self.nRu.GetValue()==True:
            self.listHeader.append("Ru")
            for nk in range(k+1): self.listHeader.append("Ru"+str(nk))
            
        # second column from GUI
        if self.nD.GetValue()==True:
            self.listHeader.append("Deg")
            for nk in range(k+1): self.listHeader.append("Deg"+str(nk))
            self.listHeader.append("inDeg")
            for nk in range(k+1): self.listHeader.append("inDeg"+str(nk))
            self.listHeader.append("outDeg")
            for nk in range(k+1): self.listHeader.append("outDeg"+str(nk))
        
        if self.nE.GetValue()==True:
            self.listHeader.append("E")
            for nk in range(k+1): self.listHeader.append("E"+str(nk))
        if self.nCl.GetValue()==True:
            self.listHeader.append("Cl")
            for nk in range(k+1): self.listHeader.append("Cl"+str(nk))
        if self.nR.GetValue()==True:
            self.listHeader.append("R")  
            for nk in range(k+1): self.listHeader.append("R"+str(nk))  
        if self.nCen.GetValue()==True:
            self.listHeader.append("Cen")
            for nk in range(k+1): self.listHeader.append("Cen"+str(nk))
        if self.nCFC.GetValue()==True:
            self.listHeader.append("CFC")
            for nk in range(k+1): self.listHeader.append("CFC"+str(nk))
        if self.nB.GetValue()==True:
            self.listHeader.append("B")
            for nk in range(k+1): self.listHeader.append("B"+str(nk))
        if self.nK.GetValue()==True:
            self.listHeader.append("K")
            for nk in range(k+1): self.listHeader.append("K"+str(nk))
        if self.nCFB.GetValue()==True:
            self.listHeader.append("CFB")
            for nk in range(k+1): self.listHeader.append("CFB"+str(nk))
        if self.nMMQ.GetValue()==True:
            self.listHeader.append("MQ")
            for nk in range(k+1): self.listHeader.append("MQ"+str(nk))
        if self.nMML.GetValue()==True:
            self.listHeader.append("ML")
            for nk in range(k+1): self.listHeader.append("ML"+str(nk))
        if self.nMMmL.GetValue()==True:
            self.listHeader.append("MmL")
            for nk in range(k+1): self.listHeader.append("MmL"+str(nk))
        if self.nAIS.GetValue()==True:
            self.listHeader.append("AIS")
            for nk in range(k+1): self.listHeader.append("AIS"+str(nk))
            self.listHeader.append("ARS")
            for nk in range(k+1): self.listHeader.append("ARS"+str(nk))
             
        TIs=len(self.listHeader)
        
        # verify the number of selected TI; if = 0 stop the application
        if TIs==0:
            self.statusbar.SetStatusText('-> Please select a Markov node descriptor and press again the Calculation button.')
            return
        self.statusbar.SetStatusText('Checking the input files ...')
        print "<> Processing directory: "+self.dirname
        print "\n<> Detected "+str(len(self.dirList))+" files: "
        for sFile in self.dirList:
            print sFile
            # checking input files for errors
            er=0
            try:
                fsFile = open(sFile,"r")
                fsFile.close()
            except IOError, error:
                dlg = wx.MessageDialog(self, 'Error opening file '+sFile+'. Please check if the file exists and try again.','MI-NODES: File Error', wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                er=1
            except UnicodeDecodeError, error:
                dlg = wx.MessageDialog(self, 'The file '+sFile+'contains at least one non-unicode characther. Please check your file and try again.' + str(error), 'MI-NODES: Unicode Error', wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                return     
            if er == 1: #if there is any open file error, the function is finishing
                return
        print "\n"

        nTI=[self.nSh.GetValue(),self.nTr.GetValue(),self.nH.GetValue(),self.nW.GetValue(),self.nS6.GetValue(),\
             self.nS.GetValue(),self.nATS.GetValue(),self.nJ.GetValue(),self.nX1.GetValue(),self.nX.GetValue(),\
             self.nG.GetValue(),self.nL.GetValue(),self.nRu.GetValue(),self.nD.GetValue(),self.nE.GetValue(),self.nCl.GetValue(),\
             self.nR.GetValue(),self.nCen.GetValue(),self.nCFC.GetValue(),self.nB.GetValue(),self.nK.GetValue(),\
             self.nCFB.GetValue(),self.nMMQ.GetValue(),self.nMML.GetValue(),self.nMMmL.GetValue(),self.nAIS.GetValue()]

        # open the output file(s)
        # resFile="_Results_DETAILS.txt" # details disabled!
        ndFile ="_Results_MDs.txt"
        sErrors="_ERRORS.txt" # for file names with errors
        
        # if resFile.find("\\")==-1: resFile=self.orig_dir+resFile
        
        # open the result files
        CentrFile = open(ndFile,"w") # output file with centralities only; over write the centrality and attack files; if no calculation, there are empty files
        
        self.statusbar.SetStatusText('Calculating node descriptors ...')
        self.Net.Enable(False)
        self.bSubmit.Enable(False)

        # header in detail file
##        frFile = open(resFile,"w") # output file with all the results
##        frFile.write("*** MI-NODES ver.2\n*** muntisa@gmail.com\n\n")
##        frFile.close() # the other routine will append additional results!
        
        # Node Header
        sHeader=self.listHeader[0] # Header with TIs
        for i in range(1,TIs): sHeader=sHeader+"\t"+self.listHeader[i]
        
        sText="Path\tNetwork\tNode\t"+sHeader       # sHeader = TIs labels
        # print sText                  # screen
        CentrFile.write(sText+"\n")  # only centrality file

        if self.nPairOut.GetValue() == True:
            # Node Header
            fPairs=open("_Results_PAIRS.txt","w")
            sHeaderP1=self.listHeader[0]+"_A" # Header with TIs for P1
            for i in range(1,TIs): sHeaderP1=sHeaderP1+"\t"+self.listHeader[i]+"_A"
                         
            sHeaderP2=self.listHeader[0]+"_B" # Header with TIs fpr P2
            for i in range(1,TIs): sHeaderP2=sHeaderP2+"\t"+self.listHeader[i]+"_B"

            sHeaderDiff=self.listHeader[0]+"_AbsDiff_AB" # differences
            for i in range(1,TIs): sHeaderDiff=sHeaderDiff+"\t"+self.listHeader[i]+"_AbsDiff_AB"

            sHeaderProd=self.listHeader[0]+"_Prod_AB" # products
            for i in range(1,TIs): sHeaderProd=sHeaderProd+"\t"+self.listHeader[i]+"_Prod_AB"

            sHeaderSum=self.listHeader[0]+"_Sum_AB" # differences
            for i in range(1,TIs): sHeaderSum=sHeaderSum+"\t"+self.listHeader[i]+"_Sum_AB"

            fPairs.write("Network_Name\tConnected\tDirected_Edges\tNetwork_Type\tNode_A\tNode_B\t"+sHeaderP1+"\t"+sHeaderP2+"\t"+sHeaderDiff+"\t"+sHeaderProd+"\t"+sHeaderSum+"\n")
            
        fErrors = open(sErrors,"w")

        # PROCESSING EACH NETWORK ----------------------------------------------------------
        nf=0
        for sFile in self.dirList:
            try:
                nf=nf+1 # index for files
                # sPath=self.Net.GetValue()
                tt1=time.clock()
                
                # frFile = open(resFile,"a") # append mode for detail file
                
                sText="* Processing: "+sFile+" ("+str(nf)+" of "+str(len(self.dirList))+") ... "
                print sText
                # frFile.write("\n"+sText+"\n")
                self.statusbar.SetStatusText(sText)
                  
                # READ the network file (MAT, NET, DAT)
                G=MCCN.ReadNetwork(sFile) # OLD # (M,labels)=MCCN.ReadNetwork(sFile)                
                vertices=int(len(G.nodes()))
                edges=int(len(G.edges()))
                sText="Initial vestices= "+str(vertices)+"\nInitial edges= "+str(edges)
                
                G=MCCN.RemoveDisconnected(G) # remove the disconnected nodes from the begining! the original graph is only with the connected nodes
                M,G_NodeList=MCCN.graph2adj(G) # get the list of nodes and connectivity matrix

                # Node degrees
                deg=array(map(float, G.degree().values()))          # vector with the degrees (float!)
                inDeg=array(map(float, G.in_degree().values()))     # vector with the in degrees (float!)
                outDeg=array(map(float, G.out_degree().values()))   # vector with the out degrees (float!)

                # Distance matrix
                d=MCCN.DistanceMatrix(G)

    ##            print "Minitial=\n", M
    ##            print "d=\n", d
    ##            print "deg=\n", deg

                # ADD WEIGHTS to M
                for i in range(len(deg)):
                    for j in range(len(deg)):
                        if M[i][j]==1:M[i][j]=deg[j] # for connected nodes use j degree as weight

    ##            print "MW=\n", M
                
                # M=array(nx.adj_matrix(G))    # OLD # recreate M without the disconnected nodes
                disconn=vertices-int(len(G.nodes()))
                sText=sText+"\nDisconnected vertices= "+str(int(disconn))+" (excluded)"
                sText=sText+"\nFinal vertices= "+str(int(len(G.nodes())))

                # writing summary for net
                print sText
                # frFile.write("\n"+sText+"\n\n")

                # String with node labels using G without disconnected points
                sLabels=""
                # OLD # G_NodeList=G.nodes() # original labels = G nodes after removed disconnected nodes
                for nl in range(len(G_NodeList)): sLabels=sLabels+str(G_NodeList[nl])+"\t"
                sLabels=sLabels[:-1]+"\n"
                
                # check dirrected or non-dirrected networks and calculate the dirrected edges
                if self.nPairOut.GetValue() == True:
                    nDirectedEdges=float(0.0) # used to decide the calculations for pairs!!!
                    for i in range(M.shape[0]):
                        for j in range(i,M.shape[1]):
                            nDirectedEdges+=abs(M[i][j]-M[j][i])
                    sNetType="Undirected" # default
                    if nDirectedEdges!=0: sNetType="Directed" # if there are directed edges

                # generate the output pairs connected and unconnected
                # get the node pair lists for connected and un-connected = Linked, Disconn
                # get the list with indices of the node pairs = indexLinked, indexDisconn
                if self.nPairOut.GetValue() == True:
                    # ----------------------------------------------------------------------
                    # get connected pairs
                    # ----------------------------------------------------------------------
                    Linked=[] # list with the disconnected pairs (P1,P2,i,j)
                    for i in range(M.shape[0]):
                        if nDirectedEdges==0:
                            initial=i
                        else:
                            initial=0
                        for j in range(initial,M.shape[1]): # if undirected initial=i (superior triangle of M only)
                            if (M[i][j]!=0) and (i!=j): # connected nodes, not the same node
                                Linked.append((G_NodeList[i],G_NodeList[j],i,j)) #append names of nodes conned
                    # remove the symetric nodes (in dirrected networks, if connections are both sense)
                    for item in Linked:
                        P11,P21,i1,j1=item
                        for check in Linked:
                            P12,P22,i2,j2=check
                            if P11==P22 and P21==P12: #if symetric pairs, remove!
                                Linked.remove(check)
                                break
                            
                    nLinked=len(Linked)
                    
                    # ----------------------------------------------------------------------
                    # get disconned pairs
                    # ----------------------------------------------------------------------
                    nDisconn=nLinked*self.NegPairs.GetValue() # x times the discconeded pairs asked by user
                    Disconn=[] # list with the disconnected pairs and indices (P1,P2,index1,index2)
     
                    # search connectivity matrix
                    for i in range(M.shape[0]):
                        if nDirectedEdges==0:
                            initial=i
                        else:
                            initial=0
                        for j in range(initial,M.shape[1]): # if undirected initial=i (superior triangle of M only)
                            if (M[i][j]==0) and (i!=j): # nodes without connectivity and not the same node
                                RndIndex=random.uniform(1, nDisconn)
                                Disconn.append((G_NodeList[i],G_NodeList[j],i,j,RndIndex)) #append names of nodes disconned

                    # remove the symetric disconnected nodes (this can happen only if the dirrected connections are double sense
                    for item in Disconn:
                        P11,P21,i1,j1,RndNo1=item
                        for check in Disconn:
                            P12,P22,i2,j2,RndNo2=check
                            if P11==P22 and P21==P12: #if symetric pairs, remove!
                                Disconn.remove(check)
                                break
                                
                    iDisconn=len(Disconn) # the index for the disconnected pairs founded
                    
                # take the path and file name from the complete name
                components = os.path.split(sFile)
                xFilex=components[1]
                xPathx=components[0]
                
                # sText="Path\tNetwork\tNode\t"+sHeader       # header for TIs
                # frFile.write(sText+"\n")

                # close the file in order to write the details from MCCN.MCCNmain
                # frFile.close()
                
                #---------------------------
                # Markov Node descriptors
                #---------------------------
                NDs=MCCN.MCCNmain(M,G_NodeList,deg,inDeg,outDeg,d,nTI,self.power.GetValue()) # matrix nodes X TIs for all k

                # frFile = open(resFile,"a") # append mode for detail file
                
                # printing the results
                for inode in range(len(G_NodeList)): # for each node
                    res=xPathx+"\t"+xFilex+"\t"+unicode(G_NodeList[inode],errors='ignore')+"\t"       # first: node label
                    for ni in range(NDs.shape[1]):
                        res=res+str(NDs[inode][ni])+"\t" # all the TIs for one node = one line of NDs
                    # print res
                    res=res[:-1]+"\n"
                    # write the outputs
                    CentrFile.write(res) # only centrality file
                    # frFile.write(res)

                # frFile.close()

                # if we are printing pair output!
                if self.nPairOut.GetValue() == True:
                    # write the output with the connected pairs
                    # "Network_Name\tConnected\tDirected_Edges\tNetwork_Type\tNode_A\tNode_B\t...."
                    for k in range(nLinked): # not lenLinked because there are free spaces
                        P1,P2,i,j=Linked[k] # pairs and indices
                        Res=xFilex+"\t1\t"+str(int(nDirectedEdges))+"\t"+sNetType+"\t"+P1+"\t"+P2+"\t"
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(NDs[i][ni])+"\t" # TIs for P1
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(NDs[j][ni])+"\t" # TIs for P2
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(abs(NDs[i][ni]-NDs[j][ni]))+"\t"
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(NDs[i][ni]*NDs[j][ni])+"\t"
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(NDs[i][ni]+NDs[j][ni])+"\t"
                            
    ##                            if nDirectedEdges==0:
    ##                                Res=Res+str(abs(NDs[I1][ni]-NDs[I2][ni]))+"\t" # undirected nets
    ##                            else:
    ##                                Res=Res+str(NDs[I1][ni]-NDs[I2][ni])+"\t" # directed nets
                                
                        fPairs.write(Res[:-1]+"\n")

                    # -----------------------------------------------------------------------------------
                    # write the output with the disconnected pairs
                    # nDisconn = no of disconnected pairs asked by use = Linked*factorFromInterface
                    # iDisconn=len(Disconn) = no of disconnected pairs founded

                    # fix how many disconnected pairs to print
                    noDisconn=iDisconn # no of disconnected pairs to be printed, default printed all founded pairs
                    if nDisconn<iDisconn: noDisconn=nDisconn # if user ask less pairs, this will be printed

                    # random sort of the disconnected pairs
                    DisconnRnd=sorted(Disconn, key=lambda student: student[4])

                    # print only a number of disconnected pairs or all
                    # the user is asking for a multiple of connected pairs but if the disconnected are less, we print what we have
                    for k in range(noDisconn): 
                        P1,P2,i,j,r=DisconnRnd[k]  
                        Res=xFilex+"\t0\t"+str(int(nDirectedEdges))+"\t"+sNetType+"\t"+P1+"\t"+P2+"\t"
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(NDs[i][ni])+"\t" # TIs for P1
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(NDs[j][ni])+"\t" # TIs for P2
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(abs(NDs[i][ni]-NDs[j][ni]))+"\t" # undirected nets
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(NDs[i][ni]*NDs[j][ni])+"\t"
                        for ni in range(NDs.shape[1]):
                            Res=Res+str(NDs[i][ni]+NDs[j][ni])+"\t"
                            
                        fPairs.write(Res[:-1]+"\n")

                tt2=time.clock()
                # print time for each file
                print "Execution Time: %(ddiffsec).2f min\n" %\
                      {"ddiffsec": (tt2-tt1)/60}
            except:
                fErrors.write(sFile+"\n")
                print "! Error for processing file: "+sFile+" ! (see _ERRORS.txt)"
                # print "Unexpected error:", sys.exc_info()[0]

        CentrFile.close()
        fErrors.close()

        if self.nPairOut.GetValue() == True:
            fPairs.close()
            
        self.Net.Enable(True)
        self.bSubmit.Enable(True)

        #os.chdir(orig_dir)
        self.statusbar.SetStatusText('Calculation finished!')

        print "->> Node descriptors => _Results_MDs.txt"

        if self.nPairOut.GetValue() == True:
            print "->> Pair file => _Results_PAIRS.txt"
        
        # print "\n(for details about the calculations, please find "+resFile+")"
        print "->> Errors => _ERRORS.txt)"
        
        # list the total execution time
        ttn=time.clock()
        print "\nTotal Execution Time: %(ddiffsec).2f min\n\n\n" %\
              {"ddiffsec": (ttn-tt0)/60}

    def OnHelp(self, event):
        frame3 = wx.Frame(None, -1, "MI-NODES Help", size=(720, 560),style=wx.CAPTION | wx.SYSTEM_MENU | wx.MINIMIZE_BOX | wx.CLOSE_BOX)
        frame3.SetIcon(wx.Icon(orig_dir+'faviconMC.ico', wx.BITMAP_TYPE_ICO))
        frame3.SetPosition((5,5))
        htlmDoc.MyHtmlPanel(frame3,-1)
        frame3.Show(True)
        
    def OnAbout(self, event):
        description = """
MI-NODES is a free Windows application that calculates the following clasical and Markov node descriptors
for any Complex Network:
- Markov-Shannon Entropy
- Markov Trace
- Markov-Harary number
- Markov-Wiener index
- Markov-Gutman topological index
- Markov-Schultz topological index (non-trivial part)
- Markov-Moreau-Broto indices
- Markov-Balaban distance connectivity index
- Markov-Randic connectivity index
- Markov-Kier-Hall indices
- Markov-Galves indices
- Markov-Leverage indices
- Markov-Rucken indice
- Markov Node Degree
- Markov Node inDegree
- Markov Node outDegree
- Markov Eccentricity
- Markov Closeness
- Markov Radiality
- Markov Centroid
- Markov Current Flow Closeness
- Markov Bargaining
- Markov-Katz status
- Markov Current Flow Betweeness 
- Markov-Marrero Quadratic form
- Markov-Marrero Linear form
- Markov-Marrero Multi-Linear form
- Markov-Avnir inverse and reflexion symmetries

All these indices are using the node probabilities resulted as a Markov normalization of
the classical connectivity matrix. The node weights are the node degrees.
It is a wxPython application that can process Pajek NET, Centibin MAT and DAT (two column data) files.
"""
        licence = """
MI-NODES ver. 2.0
Copyright © MI-NODES 2011
"""
        info = wx.AboutDialogInfo()
        #info.SetIcon(wx.Icon(self.orig_dir+'images/logoSmall.png', wx.BITMAP_TYPE_PNG))
        info.SetName('MI-NODES: MARCH-INSIDE NOde DEScriptors')
        info.SetVersion('2.0')
        info.SetDescription(description)
        info.SetCopyright('© 2011 MI-NODES')
        info.SetLicence(licence)
        info.AddDeveloper('Cristian Robert Munteanu, Spain (muntisa@gmail.com)')
        info.AddDeveloper('Humberto Gonzalez-Diaz, Spain (gonzalezdiazh@yahoo.es)')
        wx.AboutBox(info)
        
    def OnQuit(self, event):
        self.Close()
        
# main application
class MyApp(wx.App):
    def OnInit(self):
        frame = MyMenu(None, -1, 'MI-NODES: MARCH-INSIDE NOde DEScriptors')
        #frame.SetIcon(wx.Icon(orig_dir+'faviconMC.ico', wx.BITMAP_TYPE_ICO))
        frame.Centre()
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
