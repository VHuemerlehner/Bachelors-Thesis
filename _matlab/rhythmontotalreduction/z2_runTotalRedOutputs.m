allFolders = dir('./output');

for j = 1:length(allFolders)
    
    if allFolders(j).name(1) ~= '.'
        
        fprintf('Folder: %s\n', allFolders(j).name);
        
        foldName = allFolders(j).name;
        
        list = dir(sprintf('./output/%s/*.csv',foldName));
        
        for i = 1:length(list)
            totalReductionOfFIle(foldName, list(i).name);
        end
        
    end
    
end